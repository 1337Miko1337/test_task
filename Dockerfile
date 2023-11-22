FROM python

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /my_site
COPY ./requirements.txt /my_site/requirements.txt
RUN pip install -r requirements.txt

COPY . /my_site

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]