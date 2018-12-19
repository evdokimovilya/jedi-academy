from django.db import models


class Planet(models.Model):
	name = models.CharField(max_length=255, name='name')

	def __str__(self):
		return self.name

class Jedi(models.Model):
	first_name = models.CharField(max_length=255, name='first_name')
	last_name = models.CharField(max_length=255, name='last_name', blank=True, null=True)
	planet = models.ForeignKey(Planet,related_name='planet_djedaies', on_delete=models.CASCADE)
	age = models.IntegerField(name='age')
	email = models.EmailField(name='email')

	def __str__(self):
		return self.get_name()

	def get_name(self):
		if self.last_name:
			return self.first_name + ' ' + self.last_name
		else:
			return  self.first_name

	def get_link(self):
		return '/jedis/home/%d/' %(self.pk)

	def get_candidates(self):
		return Candidate.objects.filter(planet=self.planet, jedi__isnull=True)

	def get_padawans(self):
		return Candidate.objects.filter(jedi=self)


class Candidate(models.Model):
	first_name = models.CharField(max_length=255, name='first_name')
	last_name = models.CharField(max_length=255, name='last_name')
	planet = models.ForeignKey(Planet,related_name='planet', on_delete=models.CASCADE)
	age = models.IntegerField(name='age')
	email = models.EmailField(name='email')
	jedi = models.ForeignKey(Jedi, related_name='jedi_candidates', blank=True, null=True, on_delete=models.CASCADE)


	def __str__(self):
		return self.get_name()

	def get_name(self):
		return self.first_name + ' ' + self.last_name












