import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .serializer import Ad_modelSerializer
from .models import Ad_model, SpreadsheetData
from crawler.system.adscraper import geotagging
from crawler.system.webcontent import url_content_scraper
from crawler.ResponseHelper.response import ResponseHelper
from icecream import ic

def spreadsheet_modelList(request):
    if request.method == 'POST':
        try:
            keywords = request.POST.get('keyword')
            buzzwords = request.POST.get('buzzwords')
            locations = request.POST.get('location')
            
            for row_data in zip(keywords.split(','), buzzwords.split(','), locations.split(',')):
                if len(row_data) != 3:  # Make sure each row contains exactly three elements (keyword, buzzword, location)
                    return JsonResponse({'error': 'Invalid row data format'}, status=400)
                
                keyword, buzzword, location = row_data
                
                SpreadsheetData.objects.create(keyword=keyword, buzzword=buzzword, location=location)
            
            return ResponseHelper.get_success_response('Data saved successfully')
        
        except Exception as e:
            return JsonResponse({'error': 'Error saving data: {}'.format(str(e))}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

class Ad_modelList(APIView):
    def post(self, request):
        print("getting data")
        if 'csv_file' not in request.FILES:
            return ResponseHelper.get_bad_request_response('No file was uploaded')
        
        csv_file = request.FILES['csv_file']
        
        df = pd.read_csv(csv_file)
        # Get non-null values for each column
        keywords = df['keywords'].dropna()
        buzzwords = df['buzzwords'].dropna()
        locations = df['locations'].dropna()
        queries = []

        # Nested loops to generate all combinations
        for keyword in keywords:
            for buzzword in buzzwords if buzzwords.any() else [None]:
                for location in locations if locations.any() else [None]:
                    queries.append(f'{keyword} {buzzword} {location}')
        queries = ["ads", "add services"]
        try:
            for query in queries:
                looper = 0
                while looper < 15:
                    ads = url_content_scraper(query)
                    for ad in ads:
                        title = ad["title"]
                        url = ad["url"]
                        description = ad["description"]
                        screenshot = ad["screenshot"]
                        company_contact_number = ad["contact_number"]
                        company_board_members = "Not Found" #ad["company_board_members"]
                        company_email = ad["company_email"]
                        company_board_member_role = "Not Found" #ad["company_board_members_role"]
                        whois = "Not Found" #ad["whois"]

                        existing_ad = Ad_model.objects.filter(ad_url=url) or Ad_model.objects.filter(ad_title=title)
                        if existing_ad:
                            continue  

                        ad = Ad_model.objects.create(ad_url=url, ad_title=title, ad_description=description, query=query, screenshot=screenshot, company_contact_number=company_contact_number, company_board_members=company_board_members, company_email=company_email, company_board_member_role=company_board_member_role, whois=whois)
                        ad.save()
                    looper += 1
                    return ResponseHelper.get_success_response (queries,'successfully scraped data')
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(f"Error scraping data: {str(e)}")
            
    def get(self, request):
        try:
            ad = Ad_model.objects.all()
            serializer = Ad_modelSerializer(ad, many=True)
            return ResponseHelper.get_success_response(serializer.data, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
        
    
class Ad_queryOne(APIView):
    def get(self, request, query):
        try:
            ad = Ad_model.objects.filter(query=query)
            serializer = Ad_modelSerializer(ad, many=True)
            return ResponseHelper.get_success_response(serializer.data, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
        
class ads_count(APIView):
    def get(self, request):
        try:
            ad = Ad_model.objects.all().count()
            return ResponseHelper.get_success_response(ad, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))

class ad_info(APIView):
    def get(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            serializer = Ad_modelSerializer(ad)
            Ad_model.objects.filter(ad_id=ad_id).update(ad_new=False)
            return ResponseHelper.get_success_response(serializer.data, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
        
class ad_queries_count(APIView):
    def get(self, request):
        try:
            ad = Ad_model.objects.values('query').distinct().count()
            return ResponseHelper.get_success_response(ad, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))

class ad_delete(APIView):
    def delete(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            ad.delete()
            return ResponseHelper.get_success_response("Success", "Ad deleted successfully")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
    
class ad_update(APIView):
    def put(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            serializer = Ad_modelSerializer(ad, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHelper.get_success_response(serializer.data, "Success")
            return ResponseHelper.get_bad_request_response(serializer.errors)
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))

class single_ad_info(APIView):
    def get(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            # change ad_new to false
            Ad_model.objects.filter(ad_id=ad_id).update(ad_new=False)
            serializer = Ad_modelSerializer(ad)
            print(serializer.data)
            return render(request, 'ad_info.html', {"ad_info":serializer.data})
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
        
class user_single_ad_info(APIView):
    def get(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            # change ad_new to false
            Ad_model.objects.filter(ad_id=ad_id).update(ad_new=False)
            serializer = Ad_modelSerializer(ad)
            return render(request, 'user_adinfo.html', {"ad_info":serializer.data})
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
        