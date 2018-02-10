<html>
<head>
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

        % for key,value in tdic.items():
		<tr>
			<td>{{key}}</td>
			<td>{{value}}</td>
			<td>
				<a href="content_view.do?bId={{key}}">{{value}}</a></td>
			<td>{{key}}</td>
			<td>{{value}}</td>
		</tr>
		% end


		<tr>
			<td colspan="5"> <a href="write_view.do">글작성</a> </td>
		</tr>
	</table>

</body>
</html>