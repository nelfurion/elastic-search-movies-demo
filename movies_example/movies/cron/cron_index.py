from django_cron import CronJobBase, Schedule
from ..services.elasticsearch import ElasticSearchService
from ..models import Film

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        print('Cron job ran...')
        es_service = ElasticSearchService('http://127.0.0.1:9200')

        films = Film.objects.all()
        id = 1
        print('asd')
        for film in films:
            actorset = film.filmactor_set.all()
            actors = []

            for actor in actorset:
                actors.append(actor.actor.first_name + ' ' + actor.actor.last_name)


            document = {
                'title': film.title,
                'description': film.description,
                'release_year': film.release_year,
                'actors': actors
            }

            id += 1

            push_result = es_service.push('movies', 'movie', id, document)
            print(push_result)