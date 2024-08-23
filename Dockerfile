FROM ubuntu:22.04 as base
# Setup Dependecies
RUN apt-get update && apt-get upgrade -y locales --fix-missing
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils libapache2-mod-wsgi-py3
RUN apt-get install -y python3 
RUN ln /usr/bin/python3 /usr/bin/python 
RUN apt-get install -y python3-pip
RUN ln -sf /usr/bin/pip3 /usr/bin/pip 
RUN pip install --upgrade pip 

EXPOSE 80
EXPOSE 8045

RUN mkdir /var/www/rsvdemo
ADD . /var/www/rsvdemo
RUN chmod 777 -R /var/www/rsvdemo
RUN pip install -r /var/www/rsvdemo/requirements.txt

# Copy over the apache configuration file and enable the site
RUN echo "ServerName localhost" >> /etc/apache2/apache-rsvdemo.conf
COPY ./apache-docker.conf /etc/apache2/sites-available/apache-rsvdemo.conf
COPY ./ /var/www/rsvdemo/

RUN a2dissite 000-default.conf
RUN a2ensite apache-rsvdemo.conf
RUN a2enmod headers

WORKDIR /var/www/rsvdemo

CMD ["/bin/bash", "-c", "service apache2 start && tail -f /dev/null"]