# Insomnia: Losing Sleep Over REST

* smile :smile: 

0. Install prereqs
	1. [Docker Engine](https://docs.docker.com/engine/install/)
		* [Docker Compose](https://docs.docker.com/compose/install/)
	2. [Python](https://www.python.org/downloads/)[^python_version]
		* [`pip`](https://pip.pypa.io/en/stable/installing/)
	3. [Insomnia](https://insomnia.rest/)
		* Download both the client and the designer
1. Install [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) `pip3 install --user cookiecutter`
2. Start your project with cookiecutter `cookiecutter gh:agconti/cookiecutter-django-rest` [git tag :bookmark_tabs:](https://github.com/octaflop/restless/releases/tag/boilerplate)
	1. I named my project `restless` but you can name yours whatever you want to (I'll refer to the project as `restless` for this guide).
	2. `cd restless`
	3. `docker-compose up -d`
    	1. This should build a fresh docker image and start the server.
    	2. To rebuild docker images, you can always run `docker-compose build`
	3. Now you should be able to go to *`http://localhost:8000`* in a web browser and see something like the following:
	![3dfed7d3b687482f75386fe3455bbc19.png](:/4e305d77020649d18be4dcfea019aff4)
	4. To log in, you'll need to run `manage.py` commands on your django server. Because we're using django, you'll need to run `docker exec -it restless_web_1 bash`. This will put you in the command line of your django server[^docker]. Run these next commands in that server to give yourself a login.
		1. `./manage.py createsuperuser`
		2. Enter a username, email, and password.
		3. You can now try logging into the admin view: http://localhost:8000/admin/
	5. Once you can log into http://localhost:8000/admin/ you can create an API token.[^token]
		1. Go to http://localhost:8000/admin/authtoken/token/add/ and you will be able to associate a token to your username.
		2. If your username already has a token, you can retrieve it in http://localhost:8000/admin/authtoken/token/
3. Let's set up Insomnia
	1. Copy this:
	```json
	{
	  "token": "YOUR_TOKEN_HERE",
	  "host": "http://localhost:8000",
	  "api_url": "/api/v1/",
	  "user": {
	    "username": "user1",
	    "password": "1badpassword",
	    "first_name": "Tim the",
	    "last_name": "Robot",
	    "email": "tim@example.com"
	  }
	}
	```
	2. Paste it in your environment (`ctrl + E` or `cmd + E` should open the environments view). Be sure to replace `YOUR_TOKEN_HERE` with the token you made above.
		* When you make environment variables, they are accessible in Insomnia via template tags which are double curly braces `{{` `}}`. For example, we now have `{{ token }}` available as an environment variable instead of pasting the token over an over. This also lets us fill out the user form with specific references such as: `{{ user.username }}` 
	3. Add a `POST` View
		1. In the JSON body, you can simply do `{{ user | dump }}` or if you're feeling verbose:
		```json
		{
		    "username": "{{ user.username }}",
		    "password": "{{ user.password }}",
		    "first_name": "{{ user.first_name }}",
		    "last_name": "{{ user.last_name }}",
		    "email": "{{ user.email }}"
		}
		```
		Your JSON tab content should then look like ![c6f37a9663565a32af6eac42acda42d6.png](:/910f0331495443c997abf4eb6ffd7723)
	4. For the Header tab, we'll need to use our token to log in with this api.
		1. You can use `Authorization: Token {{token}}` in the *Bulk Edit* view. Your Header tab content should look like ![b724bafd8c01b7ca8e7c8252668e9598.png](:/115c9430b6d442fd85bb4586bc8589a2)
3. Let's add some more models. Personally, I like having my code solve a problem for a user, so for this project, let's suppose I am a campsite owner who needs to keep track of my camp sites and campers. I want to keep records of which camp sites are hosting which campers. Later, I want to display this on a phone app that uses this API. [git tag :bookmark_tabs:](https://github.com/octaflop/restless/releases/tag/models)
    1. We're diving back into our application's `manage.py` to help us out here, so first we'll log in with: `docker exec -it restless_web_1 bash`
	    1. Now run `./manage.py startapp campgrounds`
	    2. This will create a new app folder `campgrounds` which we will move to the `restless` main folder: `mv campgrounds/ restless/` 
	    3. We'll add this app to our main app by going to `restless/config/common.py` and adding `restless.campgrounds` to `INSTALLED_APPS`

	2. Let's add some models to our app. Models are a way to represent databases as python code. With Django, we don't have to worry about writing raw SQL (unless we want to), we simply write python classes (python objects) and relate them to each other as needed.
		1. Open `restless/campgrounds/models.py` and note that it already contains `from django.db import models`
		2. We'll add some more models as follows:
		```python
		from django.db import models
		
		class NameMixin(models.Model):
		    """Because I don't want to write the same thing over and over"""
		    name = models.CharField(max_length=255)
		
		    class Meta:
		        abstract = True
		
		    def __str__(self):
		        return f"{self.__repr__} {self.name}"
		
		
		class CampHost(NameMixin):
		    """Admins of camp campgrounds"""
		    campgrounds = models.ManyToManyField('campgrounds.Campground')
		
		
		class Camper(NameMixin):
		    """Someone staying at a campsite"""
		    campsite = models.ForeignKey('campgrounds.Campsite', on_delete=models.CASCADE,
		                                 related_name='campers')
		
		    def __str__(self):
		        ret = super(Camper).__str__()
		        return f"{ret} staying at {self.campsite.name}"
		
		
		class Campsite(NameMixin):
		    """A reservable / occupy-able location on a camp ground"""
		    tent_only = models.BooleanField(default=True)
		    location = models.CharField(max_length=255)
		    campground = models.ForeignKey('campgrounds.Campground', on_delete=models.CASCADE,
		                                   related_name='campsites')
		
		    def __str__(self):
		        ret = super(Camper).__str__()
		        return f"{ret} a campsite at {self.campground.name}"
		
		    @property
		    def hosts(self):
		        return self.campground.camphost_set.all()
		
		
		class Campground(NameMixin):
		    """A set of campsites in a location"""
		    established = models.DateTimeField(auto_now=True)
		
		    def __str__(self):
		        ret = super(Campground).__str__()
		        fmt = r"%Y-%m-%d %H:%M"
		        return f"{ret} established {self.established.strftime(fmt)}"
		
		```
    3. Note the `ForeignKey`s on `Camper` and `Campsite`. This allows us to associate many campers to campsites and many campsites to campgrounds.
    4. Note the `ManyToManyField` on `CampHost`. This allows hosts to be associated with multiple Campsites.
4. Let's add some DRF
    0. [tag `#drf`]
    1. We're going to quickly build an API for our Campsites. This is separated into a few parts:
	    1. The serializers will represent our models into a serializable structure (eg, json or csv)
	    2. Viewsets and URLs will allow us to route a path to each model's endpoint.
    2. Let's use insomnia to play with our API.
5. Generate a Schema [`./manage.py generateschema --file openapi-schema.yml`](https://www.django-rest-framework.org/api-guide/schemas/) 
    0. [tag `#schema`]
    1. Log into your django web docker again: 
    2. Install `uritemplate`: `pip install uritemplate`
    3. Generate a schema: `./manage.py generateschema > generated_schema.yml`
6. Install [Insomnia Designer](https://insomnia.rest/)
7. Open the schema
    0. [link to schema]
    1. Let's play with the designer and ensure we have well-documented examples
        0. [Link to workspace]
        1. Test Calls in insomnia
8. Bonus: Github Action
    0. Generate schema & host
    1. Test? Have we been TDD...?[^tdd]
9. Drawbacks

[^python_version]: Version 3.8 at the time of this writing, though the docker will handle the details of this for us.

[^docker]: This may seem a bit convoluted, but it allows for consistent hosting between machines. As a bonus, using docker in this way spins up a postgresql database for us to play with.

[^token]: Tom Scott gets into depth on how tokens and APIs work in one of his [videos](https://www.youtube.com/watch?v=BxV14h0kFs0).

[^tdd]: If I've been doing test-driven development, then our examples would naturally already have some tests written up already.[^ft]

[^ft]: but it turns out I didn't do as many tests as I thought.