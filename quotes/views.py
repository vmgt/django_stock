from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
	# pk_a3044a454cc94f06abffb432fb49a371

	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker_symbol']
		api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/" + ticker + "?token=pk_a3044a454cc94f06abffb432fb49a371")	
	
		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error.."

		return render(request,'home.html',{'api': api})

	else:
		return render(request,'home.html', {'ticker': "Enter a ticker symbol"})

def about(request):
	return render(request,'about.html',{})

def add_stock(request):

	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, "Stock Added successfully.")
			return redirect('add_stock')
		else:
			print(form.errors.values())
			ticker = "Error.."
			return render(request,'add_stock.html',{'ticker': form.errors.values()})
	
	else:
		ticker = Stock.objects.all()
		output = []

		for ticker_item in ticker:

			api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/" + str(ticker_item) + "?token=pk_a3044a454cc94f06abffb432fb49a371")	
		
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error.."

		return render(request,'add_stock.html',{'ticker': ticker, 'output': output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, "Stock has been deleted")
	return redirect(delete_stock)

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request,'delete_stock.html',{'ticker': ticker})
