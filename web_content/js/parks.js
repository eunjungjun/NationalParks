function states_list(json) {

   $("#state").empty();

   $("#state").append($("<option>").attr("value", "%").text("all locations"));

   for (state in json['data']) {
      $("#state").append($("<option>").attr("value", json.data[state]).text(json.data[state]));
   }
}

function results_table(json) {

   $("#results_col").empty();

   var tab = $("<table>").append(
   "<thead><th>Park Name</th><th>Location</th></thead>"
   );
   tab.width('100%');
   
   var tbody = $("<tbody>");
   tab.append(tbody);

   for (i in json['data']) {
      var rec = json['data'][i];
      var tr = $("<tr>").append(
         $("<td>").text(rec['name']).width('50%'),
         $("<td>").text(rec['state']).width('50%')
         );

      tr.attr("data-park-id", rec['park_id']);
      tr.click(function() {
         get_details($(this).attr("data-park-id"));
      });


      tbody.append(tr);
   }

   $("#results_col").append(tab);
}

function start_search() {

   var name = $("#name").val() + "%";
   var state = $("#state").val() + "%";

   $.get('/search', {"name": name, "state": state}, results_table);
}

function get_details(id) {
   $("#details").load("detailHTML", {"park_id":id}, function(){$("#details").modal()})
}

function display_facts(json) {
   $("#facts").append($("<li>").text(json['data']));

   if ($("#facts li").length == 3) {
      $("#facts_container").fadeIn();
   }
}

function get_facts() {
   $.getJSON("/fact", {}, display_facts);
}

function update_facts() {
   $("#facts_container").fadeOut(function() {
      $("#facts").empty();
      get_facts();
      get_facts();
      get_facts();
   });
}

$(document).ready(function(){

   $.get("/states", {}, states_list);

   update_facts();
   
   setInterval(update_facts, 20000);

   $("#search_form").submit(function(event){
   event.preventDefault();
   start_search();
   });
})