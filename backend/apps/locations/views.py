"""
REST API Views for SebaCox Location & Geographic Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from rest_framework import views, status, permissions
from common.responses import StandardResponse
from .selectors import (
    get_active_countries,
    get_divisions_by_country,
    get_districts_by_division,
    get_upazilas_by_district,
    get_municipalities,
    get_city_corporations,
    get_unions_by_upazila,
    get_wards,
    get_localities,
    get_postal_locations,
    get_user_locations_qs,
    get_child_locations,
)
from .serializers import (
    CountrySerializer,
    DivisionSerializer,
    DistrictSerializer,
    UpazilaSerializer,
    MunicipalitySerializer,
    CityCorporationSerializer,
    UnionSerializer,
    WardSerializer,
    LocalitySerializer,
    PostalLocationSerializer,
    UserLocationSerializer,
    LocationSearchItemSerializer,
    NearbyCalculateRequestSerializer,
    SelectedLocationUpdateSerializer,
    CurrentLocationUpdateSerializer,
)
from .services import (
    calculate_haversine_distance,
    LocationSearchService,
    UserLocationService,
)


class CountryListView(views.APIView):
    """GET /api/v1/locations/countries/ - List all active countries."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        countries = get_active_countries()
        serializer = CountrySerializer(countries, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="দেশসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class DivisionListView(views.APIView):
    """GET /api/v1/locations/divisions/?country=&country_code= - List divisions filtered by parent."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        country_id = request.query_params.get('country')
        country_code = request.query_params.get('country_code')
        divisions = get_divisions_by_country(country_id=country_id, country_code=country_code)
        serializer = DivisionSerializer(divisions, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="বিভাগসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class DistrictListView(views.APIView):
    """GET /api/v1/locations/districts/?division=&division_code= - List districts filtered by parent."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        division_id = request.query_params.get('division')
        division_code = request.query_params.get('division_code')
        districts = get_districts_by_division(division_id=division_id, division_code=division_code)
        serializer = DistrictSerializer(districts, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="জেলাসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class UpazilaListView(views.APIView):
    """GET /api/v1/locations/upazilas/?district=&district_code= - List upazilas filtered by parent."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        district_id = request.query_params.get('district')
        district_code = request.query_params.get('district_code')
        upazilas = get_upazilas_by_district(district_id=district_id, district_code=district_code)
        serializer = UpazilaSerializer(upazilas, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="উপজেলাসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class MunicipalityListView(views.APIView):
    """GET /api/v1/locations/municipalities/?district=&upazila= - List municipalities filtered by parent."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        district_id = request.query_params.get('district')
        upazila_id = request.query_params.get('upazila')
        municipalities = get_municipalities(district_id=district_id, upazila_id=upazila_id)
        serializer = MunicipalitySerializer(municipalities, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="পৌরসভাসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class CityCorporationListView(views.APIView):
    """GET /api/v1/locations/city-corporations/?district= - List city corporations."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        district_id = request.query_params.get('district')
        city_corps = get_city_corporations(district_id=district_id)
        serializer = CityCorporationSerializer(city_corps, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="সিটি কর্পোরেশনসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class UnionListView(views.APIView):
    """GET /api/v1/locations/unions/?upazila=&upazila_code= - List union parishads."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        upazila_id = request.query_params.get('upazila')
        upazila_code = request.query_params.get('upazila_code')
        unions = get_unions_by_upazila(upazila_id=upazila_id, upazila_code=upazila_code)
        serializer = UnionSerializer(unions, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="ইউনিয়নসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class WardListView(views.APIView):
    """GET /api/v1/locations/wards/?municipality=&union=&city_corporation= - List wards."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        municipality_id = request.query_params.get('municipality_id') or request.query_params.get('municipality')
        union_id = request.query_params.get('union_id') or request.query_params.get('union')
        city_corporation_id = request.query_params.get('city_corporation_id') or request.query_params.get('city_corporation')
        wards = get_wards(
            municipality_id=municipality_id,
            union_id=union_id,
            city_corporation_id=city_corporation_id
        )
        serializer = WardSerializer(wards, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="ওয়ার্ডসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class LocalityListView(views.APIView):
    """GET /api/v1/locations/localities/?upazila=&ward=&union=&municipality= - List localities."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        upazila_id = request.query_params.get('upazila_id') or request.query_params.get('upazila')
        ward_id = request.query_params.get('ward_id') or request.query_params.get('ward')
        union_id = request.query_params.get('union_id') or request.query_params.get('union')
        municipality_id = request.query_params.get('municipality_id') or request.query_params.get('municipality')
        localities = get_localities(
            upazila_id=upazila_id,
            ward_id=ward_id,
            union_id=union_id,
            municipality_id=municipality_id
        )
        serializer = LocalitySerializer(localities, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="এলাকাসমূহের তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class PostalLocationListView(views.APIView):
    """GET /api/v1/locations/postal-locations/?district=&upazila=&union=&municipality=&post_code= - List post offices."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        district_id = request.query_params.get('district')
        upazila_id = request.query_params.get('upazila')
        union_id = request.query_params.get('union')
        municipality_id = request.query_params.get('municipality')
        post_code = request.query_params.get('post_code')
        postals = get_postal_locations(
            district_id=district_id,
            upazila_id=upazila_id,
            union_id=union_id,
            municipality_id=municipality_id,
            post_code=post_code,
        )
        serializer = PostalLocationSerializer(postals, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="ডাকঘর তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class LocationSearchView(views.APIView):
    """GET /api/v1/locations/search/?q=&limit= - Search across all geographic units."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return StandardResponse.error(
                message="অনুসন্ধান করার জন্য 'q' প্যারামিটার প্রদান করুন।",
                errors={"q": ["Search query is required"]},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        limit = min(int(request.query_params.get('limit', 20)), 50)
        results = LocationSearchService.search(query=query, limit=limit)
        serializer = LocationSearchItemSerializer(results, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message=f"'{query}' এর জন্য {len(results)}টি ফলাফল পাওয়া গেছে।"
        )


class NearbyCalculateView(views.APIView):
    """
    POST /api/v1/locations/nearby/
    Calculates spherical distance between two coordinate points using Haversine formula.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = NearbyCalculateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="স্থানাঙ্ক বা তথ্য সঠিক নয়",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        distance = calculate_haversine_distance(
            lat1=data['origin_latitude'],
            lon1=data['origin_longitude'],
            lat2=data['destination_latitude'],
            lon2=data['destination_longitude'],
            unit=data.get('unit', 'km')
        )

        return StandardResponse.success(
            data={
                "origin": {
                    "latitude": float(data['origin_latitude']),
                    "longitude": float(data['origin_longitude'])
                },
                "destination": {
                    "latitude": float(data['destination_latitude']),
                    "longitude": float(data['destination_longitude'])
                },
                "distance": distance,
                "unit": data.get('unit', 'km')
            },
            message="দূরত্ব সফলভাবে গণনা করা হয়েছে।"
        )


class UserLocationListView(views.APIView):
    """GET /api/v1/locations/user/ - List all location associations for authenticated user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        loc_type = request.query_params.get('type')
        user_locations = get_user_locations_qs(user=request.user, location_type=loc_type)
        serializer = UserLocationSerializer(user_locations, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="ব্যবহারকারীর অবস্থান তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )


class UserSelectedLocationView(views.APIView):
    """
    GET, POST /api/v1/locations/user/selected/
    Reads or sets user's active SELECTED operational service area.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        selected = UserLocationService.get_selected_location(user=request.user)
        if not selected:
            return StandardResponse.success(
                data=None,
                message="কোনো সক্রিয় নির্বাচিত অবস্থান নির্ধারণ করা হয়নি।"
            )
        serializer = UserLocationSerializer(selected)
        return StandardResponse.success(
            data=serializer.data,
            message="নির্বাচিত অবস্থান সফলভাবে প্রাপ্ত হয়েছে।"
        )

    def post(self, request):
        serializer = SelectedLocationUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="প্রদত্ত তথ্য সঠিক নয়",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        user_loc = UserLocationService.set_selected_location(
            user=request.user,
            district_id=data.get('district_id'),
            upazila_id=data.get('upazila_id'),
            union_id=data.get('union_id'),
            municipality_id=data.get('municipality_id'),
            ward_id=data.get('ward_id'),
            locality_id=data.get('locality_id'),
            postal_location_id=data.get('postal_location_id'),
            detailed_address=data.get('detailed_address', ''),
            label=data.get('label', '')
        )

        return StandardResponse.success(
            data=UserLocationSerializer(user_loc).data,
            message="সেবা এলাকা সফলভাবে নির্বাচন করা হয়েছে।"
        )


class UserCurrentLocationView(views.APIView):
    """
    GET, POST /api/v1/locations/user/current/
    Reads or updates user's CURRENT GPS coordinates without modifying selected service area.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        current = UserLocationService.get_current_location(user=request.user)
        if not current:
            return StandardResponse.success(
                data=None,
                message="কোনো বর্তমান জিপিএস অবস্থান সংরক্ষিত নেই।"
            )
        return StandardResponse.success(
            data=UserLocationSerializer(current).data,
            message="বর্তমান জিপিএস অবস্থান প্রাপ্ত হয়েছে।"
        )

    def post(self, request):
        serializer = CurrentLocationUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="জিপিএস স্থানাঙ্ক সঠিক নয়",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        user_loc = UserLocationService.update_current_location(
            user=request.user,
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            address_text=data.get('address_text', '')
        )

        return StandardResponse.success(
            data=UserLocationSerializer(user_loc).data,
            message="ডিভাইসের বর্তমান অবস্থান সফলভাবে সংরক্ষিত হয়েছে।"
        )


class LocationChildrenView(views.APIView):
    """
    GET /api/v1/locations/children/?parent_type=&parent_id=
    Returns child location entities dynamically for cascading selectors.
    Supported parent_type values:
    - COUNTRY -> Divisions
    - DIVISION -> Districts
    - DISTRICT -> Upazilas
    - UPAZILA -> Unions & Municipalities
    - UNION -> Wards
    - MUNICIPALITY -> Wards
    - CITY_CORPORATION -> Wards
    - WARD -> Localities
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        parent_type = (request.query_params.get('parent_type') or '').upper().strip()
        parent_id_str = request.query_params.get('parent_id')

        if not parent_type or not parent_id_str:
            return StandardResponse.error(
                message="parent_type এবং parent_id প্যারামিটার আবশ্যক।",
                errors={"parent_type": ["Required"], "parent_id": ["Required"]},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            parent_id = int(parent_id_str)
        except (ValueError, TypeError):
            return StandardResponse.error(
                message="parent_id একটি বৈধ পূর্ণসংখ্যা হতে হবে।",
                errors={"parent_id": ["Must be an integer"]},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        children = get_child_locations(parent_type=parent_type, parent_id=parent_id)

        if parent_type == 'COUNTRY':
            data = DivisionSerializer(children, many=True).data
        elif parent_type == 'DIVISION':
            data = DistrictSerializer(children, many=True).data
        elif parent_type == 'DISTRICT':
            data = UpazilaSerializer(children, many=True).data
        elif parent_type == 'UPAZILA':
            data = {
                'unions': UnionSerializer(children.get('unions', []), many=True).data if isinstance(children, dict) else [],
                'municipalities': MunicipalitySerializer(children.get('municipalities', []), many=True).data if isinstance(children, dict) else [],
                'postal_locations': PostalLocationSerializer(children.get('postal_locations', []), many=True).data if isinstance(children, dict) else [],
            }
        elif parent_type in ['UNION', 'MUNICIPALITY', 'CITY_CORPORATION']:
            data = WardSerializer(children, many=True).data
        elif parent_type == 'WARD':
            data = LocalitySerializer(children, many=True).data
        elif parent_type == 'POSTAL':
            data = PostalLocationSerializer(children, many=True).data
        else:
            data = []

        return StandardResponse.success(
            data=data,
            message="সাব-লোকেশন তালিকা সফলভাবে প্রাপ্ত হয়েছে।"
        )

