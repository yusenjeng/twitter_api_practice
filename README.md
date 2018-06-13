# twitter_api_practice

## Installation
From [PyPi](https://pypi.python.org/pypi/kubernetes/) directly:
```
pip install -r requirements.txt
```

## Execution

Create a continuous tweets consuming task:
```
python crawler.py -lon <longitude> -lat <latitude>
```

Example:
```
python crawler.py -lon -105.301758 -lat 39.964069
```


Query the tweets form remote database:
```
python query.py -k <keywords> -lon <longitude> -lat <latitude> -r <radius in miles>
```

Example:
```
python query.py -k "#NBA Duncan" -lon -105.301758 -lat 39.964069 -r 50
```


