# django-rest
Django rest application with jwt 

<b>
for register  :: /api/signup<br>
body :: 
</b>
<pre>
{
    "email": "",
    "password": "",
    "profile": {
        "first_name": "",
        "last_name": "",
        "phone_number": "",
        "age": null,
        "gender": null
    }
}
</pre>
<b>
login endpoint :: /api/login<br>
body ::
</b>
<pre>
{
    "email": "",
    "password": ""
}
</pre>
<b>
Get profile :: /api/profile<br>
Authorization : Bearer + 'TOKEN'
</b>
