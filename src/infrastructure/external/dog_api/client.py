import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Any

from src.application.ports.output.dog_repository import DogRepository
from src.domain.entities.breed import Breed, BreedAttributes, LifeSpan, WeightRange, BreedRelationships, GroupRelationship, BreedLinks
from src.domain.entities.fact import Fact, FactAttributes
from src.domain.entities.group import Group, GroupAttributes, GroupRelationships, BreedReference
from src.domain.entities.pagination import PaginationParams, SearchParams, PaginatedResponse
from src.shared.exceptions.api_exception import APIException


class DogAPIClient(DogRepository):
    BASE_URL = "https://dogapi.dog/api/v2"

    def __init__(self):
        self._headers = {
            "Content-Type": "application/json"
        }

    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Makes an HTTP request to the API."""
        url = f"{self.BASE_URL}/{endpoint}"
        
        api_params = {}
        if params:
            if "page" in params and "page_size" in params:
                api_params["page[number]"] = params["page"]
                api_params["page[size]"] = params["page_size"]
            if "search" in params:
                api_params["filter[search]"] = params["search"]
            api_params.update({k: v for k, v in params.items() if k not in ["page", "page_size", "search"]})
        
        if api_params:
            query_string = urllib.parse.urlencode(api_params)
            url = f"{url}?{query_string}"
        
        req = urllib.request.Request(
            url,
            method=method,
            headers=self._headers,
            data=json.dumps(data).encode() if data else None
        )

        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            raise APIException(f"API Error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            raise APIException(f"Connection Error: {str(e)}")
        except json.JSONDecodeError as e:
            raise APIException(f"Error decoding response: {str(e)}")

    def _parse_breed(self, data: Dict) -> Breed:
        """Converts API data into a Breed entity."""
        breed_data = data.get("data", data)
        
        attributes = BreedAttributes(
            name=breed_data["attributes"]["name"],
            description=breed_data["attributes"].get("description"),
            life=LifeSpan(
                min=breed_data["attributes"]["life"]["min"],
                max=breed_data["attributes"]["life"]["max"]
            ) if breed_data["attributes"].get("life") else None,
            male_weight=WeightRange(
                min=breed_data["attributes"]["male_weight"]["min"],
                max=breed_data["attributes"]["male_weight"]["max"]
            ) if breed_data["attributes"].get("male_weight") else None,
            female_weight=WeightRange(
                min=breed_data["attributes"]["female_weight"]["min"],
                max=breed_data["attributes"]["female_weight"]["max"]
            ) if breed_data["attributes"].get("female_weight") else None,
            hypoallergenic=breed_data["attributes"].get("hypoallergenic", False),
           
        )

        relationships = None
        if "relationships" in breed_data and "group" in breed_data["relationships"]:
            group_data = breed_data["relationships"]["group"]["data"]
            relationships = BreedRelationships(
                group=GroupRelationship(id=group_data["id"])
            )

        links = None
        if "links" in data:
            links = BreedLinks(self=data["links"]["self"])

        return Breed(
            id=breed_data["id"],
            attributes=attributes,
            relationships=relationships,
            links=links
        )

    def _parse_group(self, data: Dict) -> Group:
        """Converts API data into a Group entity."""
        group_data = data.get("data", data)
        attributes = group_data.get("attributes", {})
        relationships = group_data.get("relationships", {})
        
        return Group(
            id=str(group_data["id"]),
            attributes=GroupAttributes(
                name=attributes["name"]
            ),
            relationships=GroupRelationships(
                breeds={
                    "data": [
                        BreedReference(id=str(breed["id"]))
                        for breed in relationships.get("breeds", {}).get("data", [])
                    ]
                }
            )
        )

    def _parse_fact(self, data: Dict) -> Fact:
        """Converts API data into a Fact entity."""
        fact_data = data.get("data", data)
        attributes = fact_data.get("attributes", {})
        
        return Fact(
            id=str(fact_data["id"]),
            type=fact_data["type"],
            attributes=FactAttributes(
                body=attributes["body"]
            )
        )

    def _filter_items(self, items: List[Any], search: Optional[SearchParams]) -> List[Any]:
        """Filters items according to search parameters."""
        if not search or not search.query:
            return items
        
        query = search.query.lower()
        return [
            item for item in items
            if any(
                str(value).lower().find(query) != -1
                for value in item.__dict__.values()
                if value is not None
            )
        ]

    def _paginate_items(self, items: List[Any], pagination: PaginationParams) -> PaginatedResponse[Any]:
        """Paginates items according to pagination parameters."""
        start_idx = (pagination.page - 1) * pagination.page_size
        end_idx = start_idx + pagination.page_size
        paginated_items = items[start_idx:end_idx]
        
        return PaginatedResponse.create(
            items=paginated_items,
            total=len(items),
            params=pagination
        )

    def get_breeds(self, pagination: PaginationParams, search: Optional[SearchParams] = None) -> PaginatedResponse[Breed]:
        """Get all dog breeds with pagination and search."""
        params = {
            "page": pagination.page,
            "page_size": pagination.page_size
        }

        if search and search.query:
            params["search"] = search.query
        response = self._make_request("breeds", params=params)
        
        breeds_data = response.get("data", [])
        meta = response.get("meta", {})
        
        breeds = [self._parse_breed({"data": breed}) for breed in breeds_data]
        
        if meta:
            return PaginatedResponse.create(
                items=breeds,
                total=meta.get("total", len(breeds)),
                params=pagination
            )

        return self._paginate_items(breeds, pagination)

    def get_breed_by_id(self, breed_id: str) -> Optional[Breed]:
        """Get a specific breed by its ID."""
        try:
            response = self._make_request(f"breeds/{breed_id}")
            return self._parse_breed(response)
        except APIException as e:
            if "404" in str(e):
                return None
            raise

    def get_facts(self) -> List[Fact]:
        """Get interesting facts about dogs."""
        response = self._make_request("facts")
        facts_data = response.get("data", [])
        return [self._parse_fact(fact) for fact in facts_data]

    def get_groups(self, pagination: PaginationParams, search: Optional[SearchParams] = None) -> PaginatedResponse[Group]:
        """Get all breed groups with pagination and search."""
        params = {
            "page": pagination.page,
            "page_size": pagination.page_size
        }
        
        if search and search.query:
            params["search"] = search.query
            
        response = self._make_request("groups", params=params)
        groups_data = response.get("data", [])
        meta = response.get("meta", {})
        
        groups = [self._parse_group(group) for group in groups_data]
        
        if meta:
            return PaginatedResponse.create(
                items=groups,
                total=meta.get("total", len(groups)),
                params=pagination
            )
        
        return self._paginate_items(groups, pagination)

    def get_group_by_id(self, group_id: str) -> Optional[Group]:
        """Get a specific group by its ID."""
        try:
            response = self._make_request(f"groups/{group_id}")
            return self._parse_group(response)
        except APIException as e:
            if "404" in str(e):
                return None
            raise

    def get_group_details(self, group_id: str) -> Optional[Group]:
        """Get complete details of a group."""
        return self.get_group_by_id(group_id)

    def get_breed_in_group(self, group_id: str, breed_id: str) -> Optional[Breed]:
        """Get a specific breed within a group."""
        group = self.get_group_details(group_id)
        if not group or not group.relationships or not group.relationships.breeds:
            return None
            
        breed_ids = [breed.id for breed in group.relationships.breeds.get("data", [])]
        if str(breed_id) not in breed_ids:
            return None
            
        return self.get_breed_by_id(breed_id) 