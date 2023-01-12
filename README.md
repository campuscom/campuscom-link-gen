This project contains a simple python script which when run with appropriate configurations and options, reads a url from the products table and generates an affiliate link using appropriate API and then saves the generated url into a field called `affiliate_link` of that particular product.

Python 3 is required to run this script. It depends on a few python modules, which must be installed with the following command:

```
pip install -r requirements.txt
```

It supports a few options. These are described below.

- `--config` : A path to a configuration file must be provided. The file must contain database configurations and the credentials for the APIs used to generate affiliate link. A sample configuration file is provided with this project. The provided file should be edited and used for this purpose. This is a _required_ option.

- `--domain`: Generate links for the products of this particular domain only. If not provided, links are generated for all the products. Value of this field must match with the domain part of the links in the product table. Therefore, based on the data available to me at this time, one of these values are valid: `www.edx.org`, `www.skillshare.com`, `www.coursera.org`, `www.datacamp.com`, `www.udemy.com`

- `--newonly`: This option does not have any value. Adding this will cause the script to skip all the products that already have a value in their respective `affiliate_link` field.

- `--retry-interval`: Sometimes APIs are throttled to allow only a definite number of requests within a particular time. In such cases, we must wait before making subsequent requests otherwise the request will fail. The value of this option is the amount of time we wait in seconds. Not providing this or passing 0 will cause the script not to retry in case of a failure due to such restrictions. Currently the retry mechanism is only implemented for Awin API.

- `--help`: Generate a brief overview of these options.


### Examples

```
python affiliatelinkgenerator/generate.py --config sample.config.json --domain www.edx.org --retry-interval 120
```

The above command will use a file called `sample.config.json` for the database access credentails and API credentials. It will then query the database for products from `www.edx.org` only. Then it will start generating affiliate links. In case it receives an HTTP Response 429 (restricted/throttled to limit number of API calls), it will wait for 120 seconds before retrying.


### TODO

- Make the name of the DB fields it reads from and writes to configurable.
- Logging improvements
- 