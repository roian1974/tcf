<p>The items are as follows:</p>
<table border="1">
  <tr>
    %for r in rows:
      <th>{{r}}</th>
    %end
  </tr>
  %for i in range(cases):
     <tr>
      %for r in rows:
        <td>{{rows[r][i]}}</td>
      %end
     </tr>
  %end
</table>