# gmailwrap


Simple wrapper around gmail api, providing a trash function.

## Install

### gmail api quickstart

follow this procedure:

[https://developers.google.com/gmail/api/quickstart/python](https://developers.google.com/gmail/api/quickstart/python)

A **credential.json** file is generated.

### module install

for example in a [virtualenv](https://virtualenv.pypa.io/en/latest/) environment,
and using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).


```
$ mkvirtualenv -p python3 gmailwrap
(gmailwrap) $ pip install -r requirements.txt
(gmailwrap) $ pip install --editable .
```

and copy **credential.json** in the cloned directory



## use

example, using virtualenvwrapper

```
$ workon gmailwrap
(gmailwrap) $ gmailwrap trash -s no-reply@dropbox.com
```
