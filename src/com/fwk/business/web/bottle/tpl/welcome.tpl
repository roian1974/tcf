<body>
%if name == 'World':
    <h1>Hello {{name}}!</h1>
    <p>This is a test.</p>
%else:
    <h1>Hello {{name.title()}}!</h1>
    <p>How are you?</p>
    <p><a href="http://localhost:8080/login">login!</a></p>
    <p><a href="http://localhost:8080/html/tcfaction.html">Visit Job Action!</a></p>
    <p><a href="http://localhost:8080/joblist">job task list!</a></p>
    <p><a href="http://localhost:8080/list">job task content!</a></p>

%end
</body>
