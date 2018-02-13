< !DOCTYPE html >
< html >
    < head >
        < meta charset = 'utf-8' >
        < title > < / title >
    < / head >
    < body > Hello.dynamic !
    %if name == 'World':
        <h1>Hello {{name_var}}!</h1>
        <p>This is a test.</p>
    %else:
        <h1>Hello {{name_var}}!</h1>
        <p>How are you?</p>
    %end
        < ul >
            {{name_var}}
        < / ul >
    < / body >
< / html >