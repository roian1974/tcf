<html>
<body>
    Welcome {{username}}<br/>
    You like <b>{{like}}</b>
<p>
<ul>
    %for thing in things:
    <li>{{thing}}</li>
    %end
</ul>
<form action="/favorite_fruits" method=POST>
    What fruit do you like ?
    <input type="text" name="fruit" size=20 value="">
    <input type="submit" value="submit">
</form>
</body>
</html>



