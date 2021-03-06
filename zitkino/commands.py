# -*- coding: utf-8 -*-


import times
from flask.ext.script import Manager, Command

from . import log
from .scrapers import scrapers
from . import __version__ as version
from .models import Cinema, Showtime


class Version(Command):
    """Print version."""

    def run(self):
        print version


class SyncShowtimes(Command):
    """Sync showtimes."""

    def _sync_showtime(self, showtime):
        if showtime.starts_at >= times.now():
            log.showtime(showtime)
            showtime.save()

    def _sync_cinema(self, cinema, showtimes):
        log.scraper(cinema.name)

        sync_start = times.now()
        counter = 0

        try:
            for showtime in showtimes:
                self._sync_showtime(showtime)
                counter += 1
        except:
            raise
        else:
            query = Showtime.objects(cinema=cinema, scraped_at__lt=sync_start)
            query.delete()
        finally:
            log.scraper('created %d showtimes', counter)

    def run(self):
        for cinema_slug, scraper in scrapers.items():
            cinema = Cinema.objects(slug=cinema_slug).get()
            showtimes = scraper()
            if showtimes:
                self._sync_cinema(cinema, showtimes)


class SyncAll(Command):
    """Sync all."""

    def run(self):
        SyncShowtimes().run()


sync = Manager(usage="Run synchronizations.")
sync.add_command('showtimes', SyncShowtimes())
sync.add_command('all', SyncAll())
