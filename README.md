# [Projet Développement & Sécurité Web | CentraleSupélec] - Santa's Little Helper
<img src="https://upload.wikimedia.org/wikipedia/fr/8/86/Logo_CentraleSup%C3%A9lec.svg" height="300px">

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)](http://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](http://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/uses-js.svg)](http://forthebadge.com)  

## Description

This web application allows members of a group to manage one or more wish lists of Christmas gifts. Members of a same group (called a Room in the application) can choose from the list of other people what they will be able to offer them. One member cannot see what other members of the Room will offer him for Xmas, Santa's Little Helper is keeping it secret so that the suprise can be total !

## Installation

Clone the repository:
```sh
git clone https://gitlab-student.centralesupelec.fr/bastien.le-guern/santas-little-helper.git
```

Type the following command at the root of the GitLab project's directory cloned on your computer: 
```sh
docker-compose up --build
```
Open a web browser (tested on Chrome & Firefox) and navigate to:
```sh
http://localhost:5000/
```
Enjoy Santa's Little Helper with your friends!

If any issues or vulnerabilities are found, please let us know in the [issues] GitLab section.(https://gitlab-student.centralesupelec.fr/bastien.le-guern/santas-little-helper/-/issues) ! 


## License

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)  
This project is licensed under the MIT License - see the [LICENSE](https://gitlab-student.centralesupelec.fr/bastien.le-guern/santas-little-helper/-/blob/master/LICENSE) file for details.


## Acknowledgments/Sources

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Flask-Security](https://pythonhosted.org/Flask-Security/)
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Flask-Talisman](https://github.com/GoogleCloudPlatform/flask-talisman)
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)

* [Docker Documentation](https://docs.docker.com/)
* [GitLab CentraleSupelec](https://gitlab-student.centralesupelec.fr/)

* [FontAwesome](https://fontawesome.com/)
* [Bulma](https://bulma.io/)
* [Google Fonts](https://fonts.google.com/)

## Developers

- [Quynh-Nhien PHAN](https://gitlab-student.centralesupelec.fr/quynh-nhien.phan)
- [Foucauld D'HEROUVILLE](https://gitlab-student.centralesupelec.fr/2018dherouvf)
- [Bastien LE GUERN](https://gitlab-student.centralesupelec.fr/bastien.le-guern)