<html>
<head>
    <h1>Document</h1>

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Insert title here</title>
</head>
<body>
	<table width="500" cellpadding="0" cellspacing="0" border="1">
		<tr>
			<td>번호</td>
			<td>이름</td>
			<td>제목</td>
			<td>날짜</td>
			<td>히트</td>
		</tr>

        % for value in tdic:
		<tr>
			<td>{{value[0]}}</td>
			<td>{{value[1]}}</td>
			<td>
				<a href="list?id={{value[2]}}">{{value[2]}}</a></td>
			<td>{{value[3]}}</td>
			<td>{{value[4]}}</td>
		</tr>
		% end

		<tr>
			<td colspan="5"> <a href="list">문서리스트</a> </td>
		</tr>
	</table>

    <p><a href="http://localhost:8080/html/tcfaction.html">Visit Job Action!</a></p>
    <p><a href="http://localhost:8080">Welcome!</a></p>


</body>
</html>