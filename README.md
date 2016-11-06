###Overview
Written in Python 3.5.2
Logs are stored in report.log file, sites list in sites_list.txt.
The checking period (CRON_FORMAT) is in web_monitor/settings.py file.

### how to:
1. `pip install -r requirements.txt`
2. `./manage.py migrate`
3. `./manage.py runserver`
4. open http://127.0.0.1:8000/
5. Register tasks with cron: `./manage.py installtasks`
6. Review the crontab: `./manage.py showtasks` or `crontab -l`
7. Run task: `./manage.py runtask run_cron`
8. See logs: `tail -f report.log`
9. Unregister task: `./manage.py uninstalltasks`
