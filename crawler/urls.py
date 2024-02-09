from crawler import views
from django.urls import path
from django.shortcuts import render

def dashboard(request):
    return render(request, 'admin_index.html')

def ads_page(request):
    return render(request, 'ads.html')

def calender(request):
    return render(request, 'calendar.html')

def search(request):
    return render(request, 'search.html')

def ad_info(request):
    return render(request, 'ad_info.html')

def dialer(request):
    return render(request, 'dialer.html')

def scraper(request):
    return render(request, 'scraper_data.html')

def spreadsheetUI(request):
    return render(request, 'spreadsheet.html')

def userads(request):
    return render(request, 'userads.html')

urlpatterns = [
    path('', userads), # dashboard page
    path('crawler/ads', ads_page), # ads page
    path('crawler/ad/<int:ad_id>', views.user_single_ad_info.as_view()), # ad info page
    path('admin/ads', ads_page), # ads page
    path('v1/scraper/ads', scraper), # scraper page
    path('crawler/dialer', dialer), # dialer page
    path('crawler/ad_info', ad_info), # ad_info page
    path('crawler/calender', calender), # calender page
    path('crawler/dashboard', dashboard), # dashboard page
    path('v1/spreadsheet', spreadsheetUI), # spreadsheet page
    path('v1/spreadsheet/data', views.spreadsheet_modelList), # spreadsheet data
    path('crawler/<int:ad_id>', views.single_ad_info.as_view()), # single ad info
    path('v1/scraper/number_of_ads', views.ads_count.as_view()), # number of ads
    path('v1/crawler/delete_ad/<int:ad_id>', views.ad_delete.as_view()), # delete ad
    path('v1/crawler/update_ad/<int:ad_id>', views.ad_update.as_view()), # update ad
    path('v1/scraper/ad_queries_count', views.ad_queries_count.as_view()), # ad queries count
]