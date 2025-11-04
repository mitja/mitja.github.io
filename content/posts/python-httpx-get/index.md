---
title: "Fetching Data from REST APIs with Python and httpx"
summary: "How to install and use httpx."
date: 2023-01-15
categories: 
  - "The Basics"
  - Blog
tags: 
  - Python
  - httpx
aliases: 
  - /blog/2023/01/15/fetching-data-from-rest-apis-with-python-and-httpx/
---

Fetching data is a common task with REST APIs. With the **httpx** module you can do it in a single command. This article shows how to install and use httpx to fetch and work with data from REST APIs.

<!-- more -->

You can perform these steps with an interactive Python prompt like ipython.

## Install httpx

Install httpx with pip.

```sh
!pip install httpx
```

## Fetch data

Next, import httpx, fetch data and store the results in a ```httpx.Response``` object. The ```response.status_code``` should be 200 for *ok*. If you see an error code such as ```404```  or an exception you may have a typo in the url.

```python
import httpx
url = 'https://api.ipify.org?format=json'
response = httpx.get(url)
response.status_code
```

## Look at the data

Use the ```content``` attribute of the response to look at the content:

```python
response.content
```

## Turn reponse content into a Python dictionary

Use the ```json()``` method to deserialize data from json to a Python dictionary.

```python
response_data = response.json()
type(response_data)
```

## Get the interesting part from the response data

Now you can use normal Python dictionary methods like ```get``` to get interesting parts of the data:

```python
ip = response_data.get('ip')
ip
```

## Send querystring parameters

Querystring parameters are appended to the url with a questionmark. They need to be encoded. With httpx you can provide a params attribute and httpx creates a querystring with parameters. Use the ip-api.com REST API to get the country for your IP address. Use the params attribute to limit the returned data to the country field. 

```python
url = f'http://ip-api.com/json/{ip}'
params = {'fields': 'country'}
response = httpx.get(url, params=params)
country = response.json().get('country')
```

Node: See [ip-api.com documentation](https://ip-api.com/docs/api:json) to learn how to use this api.

## Working with lists

When you get a list back, you can iterate over it. In the following example, you get a list of automotive manufacturers.

```python
url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmanufacturers?format=json'
response = httpx.get(url)
response_data = json()
for result in response_data.get('Results'):
    print(result.get('Mfr_Name'))
```

## Pagination

Most APIs only return a limited number of items per request. They split the result into "pages" and give you information if there are more pages and how to access them.

### Get initial results and see how many there are

Use the following code to get the first page of results from an API. This API returns power plants. If your country does not have more than 40 powerplants, please use ```'country_long': 'Germany'``` to get a large enough list for the next examples.

```python
url = ''.join([
    'https://global-power-plants.datasettes.com/',
    'global-power-plants/global-power-plants.json'
]
params = {
    'country_long': country,
    # show only 5 per page instead of default 1000
    '_size': '5', 
    # show only certain columns
    '_col': ['name', 'capacity_mw']
}
data = httpx.get(url, params=params).json()
pprint('total_plant_count: {}'.format(data.get('filtered_table_rows_count')))
plants = data.get('rows')
print('we fetched {} plants'.format(len(plants)))
```

### Get next pages of results

Like many APIs, the [Datasette API](https://docs.datasette.io/en/stable/json_api.html#special-table-arguments) provides a ```next_url``` as part of the response. Use this to fetch some more pages of results:

```python
next_url = data.get('next_url')
for page in range(3):
    data = httpx.get(next_url).json()
    plants += data.get('rows')
    next_url = data.get('next_url')
print('we fetched {} plants'.format(len(plants)))
```

## Use a client for more efficient multiple requests**

```httpx.get``` is convenient for single requests. If you want to perform many requests to the same API, you should use a ```httpx.Client```. ```httpx.Client``` is a persistent object that can reuse connections for more efficient processing. It can be used with a Python context manager like in the following example. Note how data is fetched with ```client.get``` instead of ```httpx.get```:

```python
with httpx.Client() as client:
    for i in range(4):
        data = client.get(next_url).json()
        plants += data.get('rows')
        next_url = data.get('next_url')
print('we now have fetched {} plants in total'.format(len(plants)))
```

## Authorization

Most REST APIs require authorization. There are many different variants of handling this. A very common variant is to send a ```Bearer``` token as part of the request headers. You can set this in the client or in the individual request.

```python
url = 'https://httpbin.org/bearer'
# this results in response 401 - unauthorized:
print(httpx.get(url).status_code)
headers = {
    # any text is a valid Bearer token in this demo api
    'Authorization': 'Bearer an_api_token'
}
# this result is successful (status_code 200 - OK)
print(httpx.get(url, headers=headers).status_code)
```

This is the end of this introduction to fetching data with Python and httpx. Happy coding.
