from django.urls import path, re_path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='all'),
    path('new/', views.ProductCreateView.as_view(), name='create'),
    re_path('(?P<pk>\d+)/create_review/$', views.ProductReviewCreateView.as_view(), name='create_review'),
    re_path('review/(?P<pk>\d+)/', views.ProductReviewDetailView.as_view(), name='single_review'),
    re_path('(?P<pk>\d+)/update/$', views.ProductUpdateView.as_view(), name='update'),
    re_path('(?P<pk>\d+)/dispatch/$', views.dispatchProduct, name='dispatch'),
    re_path('(?P<pk>\d+)/cancel/$', views.cancelDispatch, name='cancel'),
    re_path('(?P<pk>\d+)/delete/$', views.ProductDeleteView.as_view(), name='delete'),
    re_path('(?P<pk>\d+)/', views.ProductDetailView.as_view(), name='single'),
    re_path('by/(?P<username>[-\w]+)', views.VendorProductListView.as_view(), name='from_vendor'),
    path('search/', views.ProductSearchResultsView.as_view(), name='search'),
]
