# Overview of TheThing

TheThing comprises three building block components: 

- **[Web Crawler](https://github.com/SoheilKhodayari/JAW/tree/master/crawler):** given a single seed URL of a webapp under test, collects its webpages' resources (e.g., scripts).
- **[Static Analyzer](https://github.com/SoheilKhodayari/JAW/tree/master/analyses/domclobbering):** detects DOM Clobbering sources and sinks and potential data flows among them.
- **[Dynamic Analyzer](https://github.com/SoheilKhodayari/JAW/tree/master/dynamic):** checks the clobberability of the identified sources, and the data flows. 


The architecture of the TheThing is shown below.

<p align="center">
  <img align="center" width="900" src="https://github.com/SoheilKhodayari/TheThing/blob/master/docs/assets/architecture.png?raw=true">
</p>


## Installation

The source code of TheThing has been merged with [JAW](https://soheilkhodayari.github.io/JAW/), resulting in [JAW-v2](https://github.com/SoheilKhodayari/JAW/releases/tag/v2.0.1). This repository uses [JAW-v2](https://github.com/SoheilKhodayari/JAW/releases/tag/v2.0.1) as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).


To clone TheThing and its submodule `JAW-v2.x`, you can do:
```bash
$ git clone --recurse-submodules https://github.com/SoheilKhodayari/TheThing
```

Alternatively, do:
```bash
$ git clone https://github.com/SoheilKhodayari/TheThing
$ cd TheThing
$ git clone https://github.com/SoheilKhodayari/JAW --branch v2.0.1  
```

Then, move the JAW's content into the root directory:
```bash
$ rm JAW/.git
$ mv -rf ./JAW/* ./
```

Finally, get the necessary dependencies via:
```bash
$ ./install.sh
```

This will install the required `npm` and `python` libraries, and the `chromium` driver.


## Running the Pipeline

You can run an instance of the pipeline in a background screen via: 
```bash
$ screen -dmS s1 bash -c 'python3 -m run_domclobbering --conf=config.domclobbering.yaml; exec sh'
```

The CLI provides the following options:

```
$ python3 -m run_domclobbering -h

usage: run_domclobbering.py [-h] [--conf FILE] [--site SITE] [--list LIST] [--from FROM] [--to TO]

This script runs the tool pipeline.

optional arguments:
  -h, --help            show this help message and exit
  --conf FILE, -C FILE  pipeline configuration file. (default: config.domclobbering.yaml)
  --site SITE, -S SITE  website to test; overrides config file (default: None)
  --list LIST, -L LIST  site list to test; overrides config file (default: None)
  --from FROM, -F FROM  the first entry to consider when a site list is provided; overrides config file (default: -1)
  --to TO, -T TO        the last entry to consider when a site list is provided; overrides config file (default: -1)

```


**Configuration:** TheThing expects a `.yaml` config file as input. See [config.domclobbering.yaml](https://github.com/SoheilKhodayari/TheThing/blob/master/config.domclobbering.yaml) for an example.


## Running Building Blocks


### Crawler 

To start the [puppeteer](https://github.com/puppeteer/puppeteer)-based crawler, do:

```bash
$ node crawler.js --seedurl=https://google.com
```

Other CLI params:

- `--maxurls`: Specifies the termination criteria, i.e., the maximum number of URLs to visit
- `--browser`: Specifies the browser to use. The only option is `chrome` at the moment.
- `--headless`: Specifies whether the browser should be instantiated in `headless` mode.


For more information, see the [crawling documentation](https://github.com/SoheilKhodayari/TheThing/tree/master/docs/crawling/crawlers.md).



### Static Analyzer 

You can run the static analyzer by enabling the `static` pass in the input `.yaml` config file:

```yaml
passes:
  static: true
```

Then, in the root directory run:

```bash
$ python3 -m run_domclobbering --conf=config.yaml'
```


Alternatively, you can run the `nodejs` code for a particular `website` or `webpage` directly:

```bash
# website
$ node --max-old-space-size=4096 $(pwd)/analyses/domclobbering/static_analysis.js --seedurl=https://example.com

# webpage
$ node --max-old-space-size=4096 $(pwd)/analyses/domclobbering/static_analysis.js --singlefolder=$(pwd)/data/website-folder/webpage-folder
```


**Source Code.** The source code for the underlying static analysis engine is in the [engine](https://github.com/SoheilKhodayari/JAW/tree/master/engine) folder, whereas the vulnerability analysis code in [analyses/domclobbering](https://github.com/SoheilKhodayari/JAW/tree/master/analyses/domclobbering).

**Tests.** You will find some tests for DOM Clobbering payload generation, and source detection inside the [tests](https://github.com/SoheilKhodayari/JAW/tree/master/tests) folder.


### Dynamic Analyzer


You can run the dynamic analyzer by enabling the `dynamic` pass in the input `.yaml` config file:

```yaml
passes:
  dynamic: true
```

Then, in the root directory run:

```bash
$ python3 -m run_domclobbering --conf=config.yaml'
```

Alternatively, you can run the `nodejs` code for a particular `website` directly:


```bash
$ node --max-old-space-size=4096 $(pwd)/dynamic/force_execution.js --website=https://example.com
```

Other CLI params:

- `--browser`: the name of the browser instance
- `--use_browserstack`: whether to use a remote browser instance from [BrowserStack](https://www.browserstack.com) or not.
- `--browserstack_username`: username for BrowserStack.
- `--browserstack_password`: password for BrowserStack.
- `--browserstack_access_key`: accesskey for BrowserStack.


**Source Code.** The source code for the dynamic analysis component is in the [dynamic](https://github.com/SoheilKhodayari/JAW/tree/master/dynamic) folder.

**Tests.** You will find some tests for forced execution inside the [tests](https://github.com/SoheilKhodayari/JAW/tree/master/tests/dynamic-analysis) folder.















