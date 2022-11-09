# jmx-converter
## Yet another ... to jmx

jmx-converter is a simple python3 script that can generate Apache JMeter test plan (.jmx) from HAR

## TODO
> [X] HAR parser 
> [ ] Postman-collection parser
> [ ] Auto correlation

## Usage

Basically, all you need is python3+
To use script in default mode just run it specifying the source file

```sh
python 2jmx.py file.har
```
Also, it has some keys for configuration:
```sh
usage: 2jmx.py [-h] [-nf] [-hf] [-nh] [-j JMX] source_file

positional arguments:
  source_file         Path to source_file file. Supported types: .har

options:
  -h, --help          show this help message and exit
  -nf, --no-filter    Disables filtering out static requests
  -hf, --host-filter  Enable host filter
  -nh, --no-headers   Don't add Header Manager for samplers
  -j JMX, --jmx JMX   Custom name for .jmx
```