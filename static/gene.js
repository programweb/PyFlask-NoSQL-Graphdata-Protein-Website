$(function(){
  $('#geneList').DataTable();
  $('#geneList th:nth-child(1n+4)')
      .css({'background-color': '#d6cfe6',
        'writing-mode': 'tb-rl',
        'filter': 'flipv flipv',
        'text-align': 'right'});
  $('#geneList td .yes, #geneList td .no')
      .closest('td:nth-child(1n+3)')
      .css({'text-align':'center'});
});
