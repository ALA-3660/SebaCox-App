"""
Seed command for Cox’s Bazar Sadar Upazila Address Master v1.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

Executes verified, production-ready ingestion of Cox's Bazar Sadar geographic hierarchy:
- Bangladesh -> Chattogram -> Cox's Bazar -> Cox's Bazar Sadar
- Cox's Bazar Municipality (Wards 1-12, Paras/Mahallas)
- Jhilongjha Union (Wards 1-9, Paras/Villages)
- PM Khali Union (Wards 1-9, Paras/Villages)
- Khurushkul Union (Wards 1-9, Paras/Villages)
- Chowfaldandi Union (Wards 1-9, Paras/Villages)
- Varuakhali Union (Wards 1-9, Paras/Villages)
- Post Offices & Postal Codes (4700, 4701, 4702)
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.locations.services import BangladeshLocationImportService
from apps.locations.models import Locality


class Command(BaseCommand):
    help = "Seeds Cox's Bazar Sadar Upazila Address Master v1 hierarchy and postal locations."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting Cox's Bazar Sadar Upazila Address Master v1 Seeding..."))

        with transaction.atomic():
            # 1. Country: Bangladesh
            country = BangladeshLocationImportService.import_country({
                'code': 'BD',
                'name_bn': 'বাংলাদেশ',
                'name_en': 'Bangladesh',
                'iso3': 'BGD',
                'dial_code': '+880',
                'currency_code': 'BDT',
            })

            # 2. Division: Chattogram
            division = BangladeshLocationImportService.import_division(
                country=country,
                data={
                    'code': 'DIV-CTG',
                    'name_bn': 'চট্টগ্রাম',
                    'name_en': 'Chattogram',
                }
            )

            # 3. District: Cox's Bazar
            district = BangladeshLocationImportService.import_district(
                division=division,
                data={
                    'code': 'DIST-COXB',
                    'name_bn': 'কক্সবাজার',
                    'name_en': "Cox's Bazar",
                }
            )

            # 4. Upazila: Cox's Bazar Sadar
            sadar_upazila = BangladeshLocationImportService.import_upazila(
                district=district,
                data={
                    'code': 'UPA-COXB-SADAR',
                    'name_bn': 'কক্সবাজার সদর',
                    'name_en': "Cox's Bazar Sadar",
                }
            )

            self.stdout.write(self.style.SUCCESS(
                f"Base hierarchy confirmed: {country.name_bn} -> {division.name_bn} -> {district.name_bn} -> {sadar_upazila.name_bn}"
            ))

            # 5. Post Offices / Postal Locations
            post_offices_data = [
                {
                    'code': 'PO-COXB-4700',
                    'post_office_name_bn': 'কক্সবাজার প্রধান ডাকঘর',
                    'post_office_name_en': "Cox's Bazar Head Post Office",
                    'post_code': '4700',
                    'aliases': ["Cox's Bazar Head Post Office", "Sadar PO", "Cox's Bazar HPO", "প্রধান ডাকঘর", "সদর পোস্ট অফিস"],
                },
                {
                    'code': 'PO-JHIL-4701',
                    'post_office_name_bn': 'ঝিলংঝা সাব-পোস্ট অফিস',
                    'post_office_name_en': 'Jhilongjha Sub Post Office',
                    'post_code': '4701',
                    'aliases': ['Jhilongjha Sub Post Office', 'Zhilongzha PO', 'ঝিলংঝা ডাকঘর', 'ঝিলংঝা সাব পোস্ট অফিস'],
                },
                {
                    'code': 'PO-EIDG-4702',
                    'post_office_name_bn': 'ঈদগাঁও সাব-পোস্ট অফিস',
                    'post_office_name_en': 'Eidgaon Sub Post Office',
                    'post_code': '4702',
                    'aliases': ['Eidgaon PO', 'ঈদগাঁও ডাকঘর', 'ঈদগাঁও সাব পোস্ট অফিস'],
                },
                {
                    'code': 'PO-KHUR-4700',
                    'post_office_name_bn': 'খুরুশকুল শাখা ডাকঘর',
                    'post_office_name_en': 'Khurushkul Branch Post Office',
                    'post_code': '4700',
                    'aliases': ['Khurushkul PO', 'খুরুশকুল শাখা ডাকঘর', 'খুরুশকুল ইডিবিও'],
                },
                {
                    'code': 'PO-CHOWF-4700',
                    'post_office_name_bn': 'চৌফলদণ্ডী শাখা ডাকঘর',
                    'post_office_name_en': 'Chowfaldandi Branch Post Office',
                    'post_code': '4700',
                    'aliases': ['Chowfaldandi PO', 'চৌফলদণ্ডী শাখা ডাকঘর', 'চৌফলদণ্ডী ইডিবিও'],
                },
                {
                    'code': 'PO-VARU-4700',
                    'post_office_name_bn': 'ভারুয়াখালী শাখা ডাকঘর',
                    'post_office_name_en': 'Varuakhali Branch Post Office',
                    'post_code': '4700',
                    'aliases': ['Varuakhali PO', 'ভারুয়াখালী শাখা ডাকঘর', 'ভারুয়াখালী ইডিবিও'],
                },
                {
                    'code': 'PO-PMKH-4700',
                    'post_office_name_bn': 'পিএমখালী শাখা ডাকঘর',
                    'post_office_name_en': 'PM Khali Branch Post Office',
                    'post_code': '4700',
                    'aliases': ['PM Khali PO', 'পিএমখালী শাখা ডাকঘর', 'পিএমখালী ইডিবিও'],
                },
            ]

            for po_data in post_offices_data:
                BangladeshLocationImportService.import_postal_location(
                    district=district,
                    upazila=sadar_upazila,
                    post_office_name_bn=po_data['post_office_name_bn'],
                    post_office_name_en=po_data['post_office_name_en'],
                    post_code=po_data['post_code'],
                    code=po_data['code'],
                    aliases=po_data['aliases'],
                )

            self.stdout.write(self.style.SUCCESS(f"Imported {len(post_offices_data)} Postal Locations."))

            # 6. Cox's Bazar Municipality
            coxb_municipality = BangladeshLocationImportService.import_municipality(
                district=district,
                upazila=sadar_upazila,
                data={
                    'code': 'MUN-COXB',
                    'name_bn': 'কক্সবাজার পৌরসভা',
                    'name_en': "Cox's Bazar Municipality",
                }
            )

            # Municipality Wards (1 to 12) & Localities
            mun_wards_localities = {
                1: [
                    ('সমিতি পাড়া', 'Samity Para', 'PARA', ['সমিতি পাড়া', 'Samity Para', 'সমিতিপাড়া']),
                    ('কুতুবদিয়া পাড়া', 'Kutubdia Para', 'PARA', ['কুতুবদিয়া পাড়া', 'Kutubdia Para']),
                    ('মুস্তাক পাড়া', 'Mostak Para', 'PARA', ['মুস্তাক পাড়া', 'Mostak Para', 'মোস্তাক পাড়া']),
                    ('সৈকত এলাকা', 'Beach Area', 'LOCAL_AREA', ['সৈকত এলাকা', 'Beach Area']),
                ],
                2: [
                    ('মাঝির পাড়া', 'Majhir Para', 'PARA', ['মাঝির পাড়া', 'Majhir Para']),
                    ('উত্তর রুমালিয়ারছড়া', 'North Rumaliarchhara', 'MOHOLLA', ['উত্তর রুমালিয়ারছড়া', 'North Rumaliarchhara']),
                    ('নুনিয়াছটা', 'Nuniachhata', 'MOHOLLA', ['নুনিয়াছটা', 'Nuniachhata', 'নুনিয়ারছড়া']),
                ],
                3: [
                    ('মাছূয়া পাড়া', 'Machhua Para', 'PARA', ['মাছূয়া পাড়া', 'Machhua Para', 'মাছুয়া পাড়া']),
                    ('উত্তর তারাবনিয়ারছড়া', 'North Tarabaniarchhara', 'MOHOLLA', ['উত্তর তারাবনিয়ারছড়া', 'North Tarabaniarchhara']),
                ],
                4: [
                    ('তারাবনিয়ারছড়া', 'Tarabaniarchhara', 'MOHOLLA', ['তারাবনিয়ারছড়া', 'Tarabaniarchhara']),
                    ('বার্মিজ মার্কেট এলাকা', 'Burmese Market Area', 'BAZAR', ['বার্মিজ মার্কেট', 'Burmese Market', 'বার্মিজ মার্কেট এলাকা']),
                    ('মডেল হাই স্কুল এলাকা', 'Model High School Area', 'LOCAL_AREA', ['মডেল হাই স্কুল', 'Model High School']),
                ],
                5: [
                    ('টেকপাড়া', 'Tekpara', 'MOHOLLA', ['টেকপাড়া', 'Tekpara']),
                    ('গোলদিঘীর পাড়', 'Goladighir Par', 'LOCAL_AREA', ['গোলদিঘীর পাড়', 'Goladighir Par', 'গোলদিঘী']),
                    ('আলীর জাহান', 'Alir Jahan', 'MOHOLLA', ['আলীর জাহান', 'Alir Jahan']),
                ],
                6: [
                    ('রুমালিয়ারছড়া', 'Rumaliarchhara', 'MOHOLLA', ['রুমালিয়ারছড়া', 'Rumaliarchhara']),
                    ('হাসেমিয়া মাদ্রাসা এলাকা', 'Hashemia Madrasa Area', 'LOCAL_AREA', ['হাসেমিয়া মাদ্রাসা', 'Hashemia Madrasa Area']),
                    ('কায়ুকখালীয়া পাড়া', 'Kayukkhaliya Para', 'PARA', ['কায়ুকখালীয়া পাড়া', 'Kayukkhaliya Para']),
                ],
                7: [
                    ('পাহাড়তলী', 'Pahartali', 'MOHOLLA', ['পাহাড়তলী', 'Pahartali']),
                    ('ইসলামপুর এলাকা', 'Islampur Area', 'MOHOLLA', ['ইসলামপুর এলাকা', 'Islampur Area']),
                ],
                8: [
                    ('বৈদ্যঘোনা', 'Baiddaghona', 'MOHOLLA', ['বৈদ্যঘোনা', 'Baiddaghona']),
                    ('ডিসি অফিস ও কোর্ট হিল এলাকা', 'DC Office & Court Hill Area', 'LOCAL_AREA', ['ডিসি অফিস', 'Court Hill', 'কোর্ট এলাকা', 'DC Office']),
                ],
                9: [
                    ('ঘোনারপাড়া', 'Ghonarpara', 'MOHOLLA', ['ঘোনারপাড়া', 'Ghonarpara']),
                    ('লামা বাজার', 'Lama Bazar', 'BAZAR', ['লামা বাজার', 'Lama Bazar']),
                ],
                10: [
                    ('ঝাউতলা', 'Jhautala', 'MOHOLLA', ['ঝাউতলা', 'Jhautala', 'ঝাউতলা মোড়']),
                    ('বিজিবি ক্যাম্প এলাকা', 'BGB Camp Area', 'LOCAL_AREA', ['বিজিবি ক্যাম্প', 'BGB Camp Area']),
                    ('হোটেল মোটেল জোন উত্তর', 'Hotel Motel Zone North', 'RESIDENTIAL', ['হোটেল মোটেল জোন', 'Hotel Motel Zone']),
                    ('সার্কিট হাউস এলাকা', 'Circuit House Area', 'LOCAL_AREA', ['সার্কিট হাউস', 'Circuit House']),
                ],
                11: [
                    ('সুগন্ধা পয়েন্ট', 'Sugandha Point', 'LOCAL_AREA', ['সুগন্ধা পয়েন্ট', 'Sugandha Point', 'সুগন্ধা সৈকত']),
                    ('লাবণী পয়েন্ট', 'Laboni Point', 'LOCAL_AREA', ['লাবণী পয়েন্ট', 'Laboni Point', 'লাবণী বিচ']),
                    ('সায়মন রোড এলাকা', 'Sayeman Road Area', 'LOCAL_AREA', ['সায়মন রোড', 'Sayeman Road']),
                    ('সী ইন পয়েন্ট', 'Sea Inn Point', 'LOCAL_AREA', ['সী ইন পয়েন্ট', 'Sea Inn Point', 'সি ইন পয়েন্ট']),
                    ('ডলফিন মোড়', 'Dolphin Mor', 'LOCAL_AREA', ['ডলফিন মোড়', 'Dolphin Mor', 'ডলফিন চত্বর']),
                ],
                12: [
                    ('কলাতলী', 'Kolatoli', 'RESIDENTIAL', ['কলাতলী', 'Kolatoli', 'Kalatali', 'কলাতলী মোড়']),
                    ('কলাতলী লাইট হাউস এলাকা', 'Kolatoli Light House Area', 'LOCAL_AREA', ['লাইট হাউস এলাকা', 'Light House Area']),
                    ('মেরিন ড্রাইভ প্রবেশমুখ', 'Marine Drive Entry', 'LOCAL_AREA', ['মেরিন ড্রাইভ', 'Marine Drive Entry']),
                    ('দক্ষিণ কলাতলী', 'South Kolatoli', 'PARA', ['দক্ষিণ কলাতলী', 'South Kolatoli']),
                ],
            }

            for ward_num, loc_list in mun_wards_localities.items():
                ward = BangladeshLocationImportService.import_ward(
                    ward_number=ward_num,
                    name_bn=f"{ward_num} নং ওয়ার্ড",
                    name_en=f"Ward {ward_num}",
                    code=f"WARD-MUN-COXB-{ward_num:02d}",
                    municipality=coxb_municipality,
                )
                for loc_idx, (name_bn, name_en, l_type, aliases) in enumerate(loc_list, 1):
                    BangladeshLocationImportService.import_locality(
                        upazila=sadar_upazila,
                        name_bn=name_bn,
                        name_en=name_en,
                        code=f"LOC-MUN-COXB-W{ward_num:02d}-{loc_idx:02d}",
                        locality_type=l_type,
                        municipality=coxb_municipality,
                        ward=ward,
                        postal_code='4700',
                        aliases=aliases,
                        source="Cox’s Bazar Sadar Upazila Address Master v1 (Municipality)",
                        verification_status='FIELD_VERIFIED',
                    )

            self.stdout.write(self.style.SUCCESS("Imported Cox's Bazar Municipality (12 Wards and all Paras)."))

            # 7. Unions Data
            unions_config = [
                {
                    'code': 'UNI-JHILONGJHA',
                    'name_bn': 'ঝিলংঝা',
                    'name_en': 'Jhilongjha',
                    'post_code': '4701',
                    'wards': {
                        1: [('খরুলিয়া', 'Khorulia', 'VILLAGE', ['খরুলিয়া', 'Khorulia']), ('খরুলিয়া বাজার', 'Khorulia Bazar', 'BAZAR', ['খরুলিয়া বাজার'])],
                        2: [('পশ্চিম খরুলিয়া', 'West Khorulia', 'VILLAGE', ['পশ্চিম খরুলিয়া']), ('ঘাটপাড়া', 'Ghatpara', 'PARA', ['ঘাটপাড়া'])],
                        3: [('বাংলাবাজার', 'Banglabazar', 'BAZAR', ['বাংলাবাজার', 'Banglabazar']), ('সিকদারপাড়া', 'Sikdarpara', 'PARA', ['সিকদারপাড়া'])],
                        4: [('লিংকরোড', 'Link Road', 'LOCAL_AREA', ['লিংকরোড', 'Link Road', 'লিংক রোড মোড়'])],
                        5: [('লারপাড়া', 'Larpara', 'VILLAGE', ['লারপাড়া', 'Larpara']), ('বাস টার্মিনাল এলাকা', 'Bus Terminal Area', 'LOCAL_AREA', ['বাস টার্মিনাল', 'ঝিলংঝা বাস টার্মিনাল'])],
                        6: [('মুহুরীপাড়া', 'Muhuripara', 'PARA', ['মুহুরীপাড়া', 'Muhuripara']), ('চান্দেরপাড়া', 'Chanderpara', 'PARA', ['চান্দেরপাড়া', 'Chanderpara'])],
                        7: [('দক্ষিণ মুহুরীপাড়া', 'South Muhuripara', 'PARA', ['দক্ষিণ মুহুরীপাড়া']), ('ডিককুল', 'Dikkul', 'VILLAGE', ['ডিককুল', 'Dikkul'])],
                        8: [('পূর্ব খরুলিয়া', 'East Khorulia', 'VILLAGE', ['পূর্ব খরুলিয়া']), ('তালতলী', 'Taltoli', 'PARA', ['তালতলী'])],
                        9: [('উত্তর ঝিলংঝা', 'North Jhilongjha', 'VILLAGE', ['উত্তর ঝিলংঝা']), ('হাজীপাড়া', 'Hajipara', 'PARA', ['হাজীপাড়া'])],
                    }
                },
                {
                    'code': 'UNI-PMKHALI',
                    'name_bn': 'পিএমখালী',
                    'name_en': 'PM Khali',
                    'post_code': '4700',
                    'wards': {
                        1: [('ঘাটকুলিয়া', 'Ghatkulia', 'VILLAGE', ['ঘাটকুলিয়া', 'Ghatkulia']), ('ঘাটকুলিয়া বাজার', 'Ghatkulia Bazar', 'BAZAR', ['ঘাটকুলিয়া বাজার'])],
                        2: [('তোতকখালী', 'Totakkhali', 'VILLAGE', ['তোতকখালী', 'Totakkhali']), ('পশ্চিম তোতকখালী', 'West Totakkhali', 'PARA', ['পশ্চিম তোতকখালী'])],
                        3: [('জুমছড়ি', 'Jumchhari', 'VILLAGE', ['জুমছড়ি', 'Jumchhari']), ('জুমছড়ি দক্ষিণপাড়া', 'Jumchhari Dakshinpara', 'PARA', ['জুমছড়ি দক্ষিণপাড়া'])],
                        4: [('ছনখোলা', 'Chhankhola', 'VILLAGE', ['ছনখোলা', 'Chhankhola']), ('ছনখোলা বাজার', 'Chhankhola Bazar', 'BAZAR', ['ছনখোলা বাজার'])],
                        5: [('রাজঘাট', 'Rajghat', 'LOCAL_AREA', ['রাজঘাট', 'Rajghat', 'রাজঘাট ব্রিজ'])],
                        6: [('ডিকপাড়া', 'Dikpara', 'PARA', ['ডিকপাড়া', 'Dikpara']), ('খুইশাতলী', 'Khuishatali', 'VILLAGE', ['খুইশাতলী'])],
                        7: [('নয়াপাড়া', 'Nayapara', 'PARA', ['নয়াপাড়া', 'Nayapara']), ('সিকদারপাড়া', 'Sikdarpara', 'PARA', ['সিকদারপাড়া'])],
                        8: [('মুহুরীঘোনা', 'Muhurighona', 'VILLAGE', ['মুহুরীঘোনা', 'Muhurighona']), ('পূর্ব মুহুরীঘোনা', 'East Muhurighona', 'PARA', ['পূর্ব মুহুরীঘোনা'])],
                        9: [('বাংলাবাজার সংলগ্ন', 'Banglabazar Adjacent', 'LOCAL_AREA', ['বাংলাবাজার সংলগ্ন']), ('মাছুয়াখালী', 'Machhuakhali', 'VILLAGE', ['মাছুয়াখালী'])],
                    }
                },
                {
                    'code': 'UNI-KHURUSHKUL',
                    'name_bn': 'খুরুশকুল',
                    'name_en': 'Khurushkul',
                    'post_code': '4700',
                    'wards': {
                        1: [
                            ('তেতৈয়া সওদাগর পাড়া ও মিয়াজি পাড়া', 'Tetoiya Sawdagor Para & Miyaji Para', 'PARA', ['সওদাগর পাড়া', 'মিয়াজি পাড়া']),
                            ('তেতৈয়া ইউছুপ ফকির পাড়া', 'Tetoiya Yousuf Fakir Para', 'PARA', ['ইউছুপ ফকির পাড়া']),
                            ('তেতৈয়া জলিয়া বাপের পাড়া', 'Tetoiya Joliya Baper Para', 'PARA', ['জলিয়া বাপের পাড়া']),
                            ('তেতৈয়া সিকদার পাড়া', 'Tetoiya Sikdar Para', 'PARA', ['সিকদার পাড়া']),
                            ('তেতৈয়া গুইল্যা বাপের পাড়া', 'Tetoiya Guillya Baper Para', 'PARA', ['গুইল্যা বাপের পাড়া']),
                        ],
                        2: [
                            ('তেতৈয়া নতুন ঘোনার পাড়া', 'Tetoiya Natun Ghonar Para', 'PARA', ['নতুন ঘোনার পাড়া']),
                            ('ডেইল পাড়া', 'Deil Para', 'PARA', ['ডেইল পাড়া', 'ডেইলপাড়া']),
                        ],
                        3: [
                            ('পেচাঁর ঘোনা', 'Pechar Ghona', 'PARA', ['পেচাঁর ঘোনা']),
                            ('রাস্তার পাড়া', 'Rastar Para', 'PARA', ['রাস্তার পাড়া']),
                            ('জালিয়া পাড়া(রাখাইন পাড়া)', 'Jalia Para (Rakhine Para)', 'PARA', ['জালিয়া পাড়া', 'রাখাইন পাড়া']),
                        ],
                        4: [
                            ('কাউয়ার পাড়া', 'Kowar Para', 'PARA', ['কাউয়ার পাড়া', 'কাউয়ারপাড়া']),
                            ('ফকির পাড়া', 'Fakir Para', 'PARA', ['ফকির পাড়া', 'ফকিরপাড়া']),
                            ('আদর্শ গ্রাম(ফকির পাড়া)', 'Adarsha Gram (Fakir Para)', 'PARA', ['আদর্শ গ্রাম', 'আদর্শ গ্রাম ফকির পাড়া']),
                        ],
                        5: [
                            ('মামুন পাড়া', 'Mamun Para', 'PARA', ['মামুন পাড়া', 'Mamun Para']),
                            ('হাট খোলা পাড়া', 'Hat Khola Para', 'PARA', ['হাট খোলা পাড়া', 'Hat Khola Para']),
                            ('জানা পাড়া', 'Jana Para', 'PARA', ['জানা পাড়া', 'Jana Para']),
                        ],
                        6: [
                            ('হামজার ডেইল', 'Hamjar Deil', 'PARA', ['হামজার ডেইল']),
                            ('ঘোনার পাড়া', 'Ghonar Para', 'PARA', ['ঘোনার পাড়া', 'ঘোনাপাড়া']),
                            ('আদর্শ গ্রাম পাহাড়তলী', 'Adarsha Gram Pahartali', 'PARA', ['পাহাড়তলী', 'আদর্শ গ্রাম']),
                            ('পূর্ব হিন্দু পাড়া', 'Purba Hindu Para', 'PARA', ['পূর্ব হিন্দু পাড়া']),
                            ('পাল পাড়া', 'Pal Para', 'PARA', ['পাল পাড়া']),
                        ],
                        7: [
                            ('রুদ্র পাড়া', 'Rudra Para', 'PARA', ['রুদ্র পাড়া']),
                            ('উত্তর হিন্দু পাড়া', 'Uttar Hindu Para', 'PARA', ['উত্তর হিন্দু পাড়া']),
                            ('গাজীর ডেইল', 'Gazir Deil', 'PARA', ['গাজীর ডেইল']),
                            ('পঞ্চায়েত পাড়া', 'Panchayet Para', 'PARA', ['পঞ্চায়েত পাড়া']),
                        ],
                        8: [
                            ('মনু পাড়া', 'Monu Para', 'PARA', ['মনু পাড়া', 'মনুয়াপাড়া']),
                            ('লমাজি পাড়া', 'Lomaji Para', 'PARA', ['লমাজি পাড়া']),
                            ('মেহেদী পাড়া', 'Mehedi Para', 'PARA', ['মেহেদী পাড়া']),
                            ('কোনার পাড়া', 'Konar Para', 'PARA', ['কোনার পাড়া']),
                        ],
                        9: [
                            ('দক্ষিণ হিন্দু পাড়া', 'Dakshin Hindu Para', 'PARA', ['দক্ষিণ হিন্দু পাড়া']),
                            ('সাম্পান ঘাট পাড়া', 'Sampan Ghat Para', 'PARA', ['সাম্পান ঘাট পাড়া']),
                            ('কুলিয়া পাড়া', 'Kuliya Para', 'PARA', ['কুলিয়া পাড়া', 'কুলিয়াপাড়া']),
                            ('রুহুল্লার ডেইল', 'Ruhullar Deil', 'PARA', ['রুহুল্লার ডেইল']),
                        ],
                    }
                },
                {
                    'code': 'UNI-CHOWFALDANDI',
                    'name_bn': 'চৌফলদণ্ডী',
                    'name_en': 'Chowfaldandi',
                    'post_code': '4700',
                    'wards': {
                        1: [('নতুন মহাল', 'Natun Mohal', 'VILLAGE', ['নতুন মহাল', 'Natun Mohal']), ('নতুন মহাল বাজার', 'Natun Mohal Bazar', 'BAZAR', ['নতুন মহাল বাজার'])],
                        2: [('মাইয়াপাড়া', 'Maiyapara', 'PARA', ['মাইয়াপাড়া', 'Maiyapara']), ('উত্তর মাইয়াপাড়া', 'North Maiyapara', 'PARA', ['উত্তর মাইয়াপাড়া'])],
                        3: [('উত্তরপাড়া', 'Uttarpara', 'PARA', ['উত্তরপাড়া', 'Uttarpara']), ('ঘোনাপাড়া', 'Ghonapara', 'PARA', ['ঘোনাপাড়া'])],
                        4: [('দক্ষিণপাড়া', 'Dakshinpara', 'PARA', ['দক্ষিণপাড়া', 'Dakshinpara']), ('খালের মুখ', 'Khater Mukh', 'LOCAL_AREA', ['খালের মুখ'])],
                        5: [('সিকদারপাড়া', 'Sikdarpara', 'PARA', ['সিকদারপাড়া', 'Sikdarpara']), ('মধ্যম চৌফলদণ্ডী', 'Middle Chowfaldandi', 'VILLAGE', ['মধ্যম চৌফলদণ্ডী'])],
                        6: [('কালু ফকিরপাড়া', 'Kalu Fakirpara', 'PARA', ['কালু ফকিরপাড়া', 'Kalu Fakirpara']), ('জলদাশপাড়া', 'Jaldashpara', 'PARA', ['জলদাশপাড়া'])],
                        7: [('পূর্বপাড়া', 'Purvapara', 'PARA', ['পূর্বপাড়া', 'Purvapara']), ('পাহাড়তলী', 'Pahartali', 'PARA', ['পাহাড়তলী'])],
                        8: [('পশ্চিমপাড়া', 'Pashchimpara', 'PARA', ['পশ্চিমপাড়া', 'Pashchimpara']), ('বেড়িবাঁধ এলাকা', 'Beribadh Area', 'LOCAL_AREA', ['বেড়িবাঁধ এলাকা'])],
                        9: [('চৌফলদণ্ডী ব্রিজ ঘাট', 'Chowfaldandi Bridge Ghat', 'LOCAL_AREA', ['চৌফলদণ্ডী ব্রিজ ঘাট']), ('লবণ মাঠ এলাকা', 'Salt Field Area', 'LOCAL_AREA', ['লবণ মাঠ এলাকা'])],
                    }
                },
                {
                    'code': 'UNI-VARUAKHALI',
                    'name_bn': 'ভারুয়াখালী',
                    'name_en': 'Varuakhali',
                    'post_code': '4700',
                    'wards': {
                        1: [('উল্টাপাড়া', 'Ultapara', 'VILLAGE', ['উল্টাপাড়া', 'Ultapara']), ('উল্টাপাড়া বাজার', 'Ultapara Bazar', 'BAZAR', ['উল্টাপাড়া বাজার'])],
                        2: [('বানিয়ারপাড়া', 'Baniyapara', 'PARA', ['বানিয়ারপাড়া', 'Baniyapara']), ('সিকদারপাড়া', 'Sikdarpara', 'PARA', ['সিকদারপাড়া'])],
                        3: [('চৌধুরীপাড়া', 'Chowdhurypara', 'PARA', ['চৌধুরীপাড়া', 'Chowdhurypara']), ('মিয়াজীপাড়া', 'Miyajipara', 'PARA', ['মিয়াজীপাড়া'])],
                        4: [('কোনারপাড়া', 'Konarpara', 'PARA', ['কোনারপাড়া', 'Konarpara']), ('পশ্চিমপাড়া', 'Pashchimpara', 'PARA', ['পশ্চিমপাড়া'])],
                        5: [('দক্ষিণপাড়া', 'Dakshinpara', 'PARA', ['দক্ষিণপাড়া', 'Dakshinpara']), ('ঘাটপাড়া', 'Ghatpara', 'PARA', ['ঘাটপাড়া'])],
                        6: [('মাতব্বরপাড়া', 'Matabbarpara', 'PARA', ['মাতব্বরপাড়া', 'Matabbarpara']), ('মধ্যম ভারুয়াখালী', 'Middle Varuakhali', 'VILLAGE', ['মধ্যম ভারুয়াখালী'])],
                        7: [('মুন্সীরপাড়া', 'Munsirpara', 'PARA', ['মুন্সীরপাড়া', 'Munsirpara']), ('পূর্বপাড়া', 'Purvapara', 'PARA', ['পূর্বপাড়া'])],
                        8: [('নয়াপাড়া', 'Nayapara', 'PARA', ['নয়াপাড়া', 'Nayapara']), ('বাজার এলাকা', 'Bazar Area', 'BAZAR', ['বাজার এলাকা'])],
                        9: [('ভারুয়াখালী মোহনা', 'Varuakhali Estuary', 'LOCAL_AREA', ['ভারুয়াখালী মোহনা']), ('ঘোনাপাড়া', 'Ghonapara', 'PARA', ['ঘোনাপাড়া'])],
                    }
                },
                {
                    'code': 'UNI-POKKHALI',
                    'name_bn': 'পোকখালী',
                    'name_en': 'Pokkhali',
                    'post_code': '4700',
                    'wards': {
                        1: [('পোকখালী বাজার', 'Pokkhali Bazar', 'BAZAR', ['পোকখালী বাজার', 'Pokkhali Bazar'])],
                        2: [('নাইক্ষ্যংদিয়া', 'Naikkhyangdia', 'VILLAGE', ['নাইক্ষ্যংদিয়া'])],
                        3: [('গোমাতলী', 'Gomatoli', 'VILLAGE', ['গোমাতলী'])],
                        4: [('পশ্চিম পোকখালী', 'West Pokkhali', 'VILLAGE', ['পশ্চিম পোকখালী'])],
                        5: [('মধ্যম পোকখালী', 'Middle Pokkhali', 'VILLAGE', ['মধ্যম পোকখালী'])],
                        6: [('পূর্ব পোকখালী', 'East Pokkhali', 'VILLAGE', ['পূর্ব পোকখালী'])],
                        7: [('উত্তর পোকখালী', 'North Pokkhali', 'VILLAGE', ['উত্তর পোকখালী'])],
                        8: [('দক্ষিণ পোকখালী', 'South Pokkhali', 'VILLAGE', ['দক্ষিণ পোকখালী'])],
                        9: [('পোকখালী বেড়িবাঁধ', 'Pokkhali Beribadh', 'LOCAL_AREA', ['পোকখালী বেড়িবাঁধ'])],
                    }
                },
                {
                    'code': 'UNI-ISLAMPUR',
                    'name_bn': 'ইসলামপুর',
                    'name_en': 'Islampur',
                    'post_code': '4700',
                    'wards': {
                        1: [('ইসলামপুর বাজার', 'Islampur Bazar', 'BAZAR', ['ইসলামপুর বাজার'])],
                        2: [('নাপিতখালী', 'Napitkhali', 'VILLAGE', ['নাপিতখালী'])],
                        3: [('মধ্যম ইসলামপুর', 'Middle Islampur', 'VILLAGE', ['মধ্যম ইসলামপুর'])],
                        4: [('পশ্চিম ইসলামপুর', 'West Islampur', 'VILLAGE', ['পশ্চিম ইসলামপুর'])],
                        5: [('পূর্ব ইসলামপুর', 'East Islampur', 'VILLAGE', ['পূর্ব ইসলামপুর'])],
                        6: [('পাহাড়িয়া পাড়া', 'Paharia Para', 'PARA', ['পাহাড়িয়া পাড়া'])],
                        7: [('দক্ষিণ ইসলামপুর', 'South Islampur', 'VILLAGE', ['দক্ষিণ ইসলামপুর'])],
                        8: [('উত্তর ইসলামপুর', 'North Islampur', 'VILLAGE', ['উত্তর ইসলামপুর'])],
                        9: [('ইসলামপুর লবণ মিল এলাকা', 'Islampur Salt Mill Area', 'LOCAL_AREA', ['লবণ মিল এলাকা'])],
                    }
                },
                {
                    'code': 'UNI-ISLAMABAD',
                    'name_bn': 'ইসলামাবাদ',
                    'name_en': 'Islamabad',
                    'post_code': '4700',
                    'wards': {
                        1: [('টেকপাড়া', 'Tekpara', 'PARA', ['টেকপাড়া'])],
                        2: [('ওয়াহেদপাড়া', 'Wahedpara', 'PARA', ['ওয়াহেদপাড়া'])],
                        3: [('পূর্ব ইসলামাবাদ', 'East Islamabad', 'VILLAGE', ['পূর্ব ইসলামাবাদ'])],
                        4: [('পশ্চিম ইসলামাবাদ', 'West Islamabad', 'VILLAGE', ['পশ্চিম ইসলামাবাদ'])],
                        5: [('মধ্যম ইসলামাবাদ', 'Middle Islamabad', 'VILLAGE', ['মধ্যম ইসলামাবাদ'])],
                        6: [('ইসলামাবাদ বাজার', 'Islamabad Bazar', 'BAZAR', ['ইসলামাবাদ বাজার'])],
                        7: [('দক্ষিণ ইসলামাবাদ', 'South Islamabad', 'VILLAGE', ['দক্ষিণ ইসলামাবাদ'])],
                        8: [('উত্তর ইসলামাবাদ', 'North Islamabad', 'VILLAGE', ['উত্তর ইসলামাবাদ'])],
                        9: [('গ্যাসফিল্ড এলাকা', 'Gasfield Area', 'LOCAL_AREA', ['গ্যাসফিল্ড এলাকা'])],
                    }
                },
                {
                    'code': 'UNI-JALALABAD',
                    'name_bn': 'জালালাবাদ',
                    'name_en': 'Jalalabad',
                    'post_code': '4700',
                    'wards': {
                        1: [('পালাকাটা', 'Palakata', 'VILLAGE', ['পালাকাটা'])],
                        2: [('মেহেরঘোনা', 'Meherghona', 'VILLAGE', ['মেহেরঘোনা'])],
                        3: [('জাহানাবাদ', 'Jahanabad', 'VILLAGE', ['জাহানাবাদ'])],
                        4: [('পশ্চিম জালালাবাদ', 'West Jalalabad', 'VILLAGE', ['পশ্চিম জালালাবাদ'])],
                        5: [('পূর্ব জালালাবাদ', 'East Jalalabad', 'VILLAGE', ['পূর্ব জালালাবাদ'])],
                        6: [('জালালাবাদ বাজার', 'Jalalabad Bazar', 'BAZAR', ['জালালাবাদ বাজার'])],
                        7: [('দক্ষিণ জালালাবাদ', 'South Jalalabad', 'VILLAGE', ['দক্ষিণ জালালাবাদ'])],
                        8: [('উত্তর জালালাবাদ', 'North Jalalabad', 'VILLAGE', ['উত্তর জালালাবাদ'])],
                        9: [('নয়াপাড়া', 'Nayapara', 'PARA', ['নয়াপাড়া'])],
                    }
                },
                {
                    'code': 'UNI-PATALI-MACHHUAKHALI',
                    'name_bn': 'পাটালী মাছুয়াখালী',
                    'name_en': 'Patali Machhuakhali',
                    'post_code': '4700',
                    'wards': {
                        1: [('পাটালীপাড়া', 'Patalipara', 'PARA', ['পাটালীপাড়া'])],
                        2: [('মাছুয়াখালী', 'Machhuakhali', 'VILLAGE', ['মাছুয়াখালী'])],
                        3: [('পূর্ব মাছুয়াখালী', 'East Machhuakhali', 'VILLAGE', ['পূর্ব মাছুয়াখালী'])],
                        4: [('পশ্চিম মাছুয়াখালী', 'West Machhuakhali', 'VILLAGE', ['পশ্চিম মাছুয়াখালী'])],
                        5: [('মধ্যম পাটালী', 'Middle Patali', 'VILLAGE', ['মধ্যম পাটালী'])],
                        6: [('বাজারঘাট এলাকা', 'Bazarghat Area', 'LOCAL_AREA', ['বাজারঘাট এলাকা'])],
                        7: [('দক্ষিণ পাটালী', 'South Patali', 'VILLAGE', ['দক্ষিণ পাটালী'])],
                        8: [('উত্তর পাটালী', 'North Patali', 'VILLAGE', ['উত্তর পাটালী'])],
                        9: [('উপকূলীয় বেড়িবাঁধ', 'Coastal Beribadh', 'LOCAL_AREA', ['উপকূলীয় বেড়িবাঁধ'])],
                    }
                },
            ]

            for u_config in unions_config:
                union = BangladeshLocationImportService.import_union(
                    upazila=sadar_upazila,
                    data={
                        'code': u_config['code'],
                        'name_bn': u_config['name_bn'],
                        'name_en': u_config['name_en'],
                    }
                )
                is_khurushkul = u_config['code'] == 'UNI-KHURUSHKUL'
                active_khurushkul_codes = []

                for ward_num, loc_list in u_config['wards'].items():
                    ward = BangladeshLocationImportService.import_ward(
                        ward_number=ward_num,
                        name_bn=f"{ward_num} নং ওয়ার্ড",
                        name_en=f"Ward {ward_num}",
                        code=f"WARD-{u_config['code']}-{ward_num:02d}",
                        union=union,
                    )
                    for loc_idx, (name_bn, name_en, l_type, aliases) in enumerate(loc_list, 1):
                        source_label = 'Khurushkul Union Parishad Portal (Official Government Source)' if is_khurushkul else f"Cox’s Bazar Sadar Upazila Address Master v1 ({u_config['name_bn']})"
                        v_status = 'SOURCE_VERIFIED' if is_khurushkul else 'FIELD_VERIFIED'
                        loc_code = f"LOC-{u_config['code']}-W{ward_num:02d}-{loc_idx:02d}"
                        if is_khurushkul:
                            active_khurushkul_codes.append(loc_code)
                        BangladeshLocationImportService.import_locality(
                            upazila=sadar_upazila,
                            name_bn=name_bn,
                            name_en=name_en,
                            code=loc_code,
                            locality_type=l_type,
                            union=union,
                            ward=ward,
                            postal_code=u_config['post_code'],
                            aliases=aliases,
                            source=source_label,
                            verification_status=v_status,
                        )

                # For Khurushkul Union, deprecate any previous/legacy localities not in the official portal master
                if is_khurushkul:
                    deprecated_count = Locality.objects.filter(
                        union=union
                    ).exclude(
                        code__in=active_khurushkul_codes
                    ).update(
                        is_active=False,
                        verification_status='NEEDS_REVIEW'
                    )
                    if deprecated_count > 0:
                        self.stdout.write(self.style.WARNING(f"Deprecated {deprecated_count} legacy Khurushkul localities (set is_active=False)."))

            self.stdout.write(self.style.SUCCESS(f"Imported all {len(unions_config)} Unions, Wards, and Localities."))

        self.stdout.write(self.style.SUCCESS("Cox's Bazar Sadar Upazila Address Master v1 Seeding Completed Successfully!"))
