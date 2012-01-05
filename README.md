# linuxmagazine

linuxmagazine es un script que permite la sincronización de los artículos de la web Linux Magazine (http://linux-magazine.es/).
Se podrán sincronizar todos los artículos para los clientes con suscripción digital o los artículos libres.

## Requeriments

$ sudo apt-get install git
$ sudo apt-get install python-setuptools python-virtualenv python-pip

## Installation

$ virtualenv --no-site-packages --distribute linuxmagazine
$ cd linuxmagazine
$ . bin/activate
$ git clone git@github.com:b3ni/linuxmagazine.git src
$ cd src

virtualenv linuxmagazine
cd linuxmagazine
source bin/activate
git clone git@github.com:b3ni/linuxmagazine.git
pip install -E . -r src/requeriments.txt

## Usage

Dentro de: linuxmagazine/src

Para sincronizar la copia local con los archivos de la web:

$ python linuxmagazine.py sync

## Configuration

Editar el fichero linuxmagazine/src/config.py

DIR_STORE = 'store'

Indica en directorio guardar los archivos descargados

USER = ''
PASS = ''

Usuario y password para la suscripción digital

## License
