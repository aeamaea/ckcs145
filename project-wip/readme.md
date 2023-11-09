CKCS145 - Full Stack Developer Final Project. by Amr Malik

Technologies used:
	Python, Flask, Flask-login, MongoDB, Mongo-engine (ORM), Bootstrap, HTML5, CSS

- Main page (SPA) application with multiple sections
- A Delivery cost calculator which uses values stored in a backend mongodb collection 
  to calculate delivery costs and shows them on the page via AJAX without reloading the page
- A contact form which takes values from the user and saves them in the backend database.
- All user visits are recorded in the Visitors collection with IP and time of visit.
- 
- An ADMIN interface which the user has to login to with the user/password verified against a 
  backend (mongodb) and user is granted a session
- Admin users can edit the "weight and distance coefficients" in the coefficients table. These 
  coefficients are used in calculating the delivery cost for regular users of the website.
- Session invalidation and logout which prohibits access to the /admin route
