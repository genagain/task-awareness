# Task Awareness

This software allows me to determine what I've done during the course of a day. Because the data will be stored in a database, I'll be able to review what I've done during the course of a week, month and year assuming that I have the requisite data. 

This software is written in Python 3.

The following function invocation lists the cards I've archived in a given day.

```
from taskawareness import trello
trello.get_archived_cards('2019-01-09')
```

The above function invocation returns the following output.

```
[
  'Pack stationary for work'
]
```

The following function invocation lists the check list items I've completed in a given day.

```
from taskawareness import trello
trello.get_completed_items('2019-01-09')
```

The above function invocation returns the following output.

```
[
  'Find blue cross blue shield card on Get a therapist',
  'Do laundry on Laundry',
  'Fold laundry on Laundry',
  'Write README that describes set up and intended use on Trello diff report'
]
```

If you were to run the following function invocation on January 20, 2019 you would get all of the check list items I've completed and card's I've archived from January 13, 2019 to January 19, 2019, which is the week prior

```
from taskawareness import trello
trello.generate_report('week to day')
```

#TODO add expected output for a report for a week of January 13, 2019 to January 19, 2019

If you were to run the same function invocation as above on January 24, 2019 you would get all of the check list items I've completed and card's I've archived from January 20, 2019 to January 23, 2019.

#TODO add expected output for a report for a week of January 20, 2019 to January 23, 2019
