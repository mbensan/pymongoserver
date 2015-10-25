var baseDir = "http://localhost:8000/api/";
var USUARIO = null;


// setea direcciones.
$('#form_register').attr('action', baseDir+'signup/');
$('#form_login').attr('action', baseDir+'login/');
$('#form_add_need').attr('action', baseDir+'add_need/');

/*
str x str x str => void
 */
function show_alert(mensaje, pagina, tipo){
  div_alert = $('div#' + pagina + ' div.alert-' + tipo);
  div_alert.find('span.mensaje').html(mensaje);
  div_alert.css('display', 'block');
}


/**
 * Muestra los erroes de un formulario en los correspondientes span
 * @param  {[Object]} form_errors [DIccionario ocn los errores]
 * @param  {[String]} fo
 * rm_name   [Nombre del formulario]
 * @return {[void]}
 */
function show_form_errors(form_errors, form_name){
  for (var property in form_errors) {
    form = $('#'+form_name);

    if (form_errors.hasOwnProperty(property)) {
        form.find('input[name="'+property+'"]')
          .after('<p class="form-error"><span><strong>Error:</strong> '+form_errors[property]+'</span></p>');
    }
  }
}


/**
 * Esconde toods los errores de una pagina
 * @param  {[String]} pagina [id de la pagina]
 * @return {[void]}
 */
function hide_all(pagina){
  $('#'+pagina+' div.alert').css('display', 'none');
  $('#'+pagina+' p.form-error').remove();
}


/**
 * Carga los datos de los needs en el DOM
 * @return {[void]}
 */
function cargar_needs_dom(){
  $('form#form_add_need input[name="usuario_email"]').val(USUARIO.email);

  lista_needs = $('#lista_needs');
  lista_needs.html('');
  needs = USUARIO.needs;

  for(var i = 0; i < needs.length; ++i){
    var descripcion = needs[i].descripcion;
    var tipo = needs[i].tipo;
    $('#lista_needs').append('<li>'
      + '<img src="img/btn_'+tipo+'.png"/><a href="#need_page" data-need="'+descripcion+'">'
      + '<span class="descripcion">'+descripcion+'</span><span class="ui-li-count">0</span></a></li>');
  }
  $('#lista_needs').listview('refresh');
}


function agregar_need_dom(nuevo_need){
  lista_needs = $('#lista_needs');
  lista_needs.append('<li>'
    + '<img src="img/btn_'+nuevo_need.tipo+'.png"/><a href="#need_page" data-need="'+descripcion+'">'
    + '<span class="descripcion">'+nuevo_need['descripcion']+'</span><span class="ui-li-count">0</span></a></li>');
  lista_needs.listview('refresh');
}


$(document).bind('pageinit',function(){
  $('div:jqmData(role="page")').live('pagebeforeshow',function(e){
    if($(this).attr('id') == 'map_page'){
      
      var myLatlng = new google.maps.LatLng(-40.65, -73.95);
      var myOptions = {
      zoom: 15,
      center: myLatlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
      
      // centrar el mapa
      if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(
        function(position){
          //alert(position.coords.latitude+' -- '+(position.coords.longitude));
          map.setCenter(new google.maps.LatLng(position.coords.latitude, position.coords.longitude), 15);
        },
        function(error){
          alert(error);
        });
        
      } else {
        alert('Su dispositivo no soporta Geolocalización');
      }
  
    } else if($(this).attr('id') == 'list_page') {
      cargar_needs_dom();

      $('ul#lista_needs a').click(function(e){
        var need_descripcion = $(this).attr('data-need');
        localStorage.setItem('need_para_lista_matches', need_descripcion);
      });

    } else if($(this).attr('id') == 'need_page'){

      var need_descripcion = localStorage.getItem('need_para_lista_matches');
      var matches = JSON.parse(localStorage.getItem('matches'));
      console.log(matches);

      var lista_matches = $('ul#lista_matches');
      lista_matches.html('');

      for(var i=0 ; i<matches.length; ++i){

        if (need_descripcion === matches[i]['need_consultor_descripcion']){
          need_consultado_descripcion = matches[i]['need_consultado_descripcion'];
          need_consultado_tipo = matches[i]['need_consultado_tipo'];
          nombre_consultado = matches[i]['nombre_consultado'];
          email_consultado = matches[i]['email_consultado'];

          lista_matches.append('<li>'
            +'<img src="img/btn_'+need_consultado_tipo+'.png"/>'
            +'<h4>'+need_consultado_descripcion+'</h4>'
            +'<p>Usuario: <b>'+nombre_consultado+'</b></p>'
            +'<p>Email: <b>'+email_consultado+'</b></p>'
            +'</li>');
        }
      }
      lista_matches.listview('refresh');
    }
  });
});


$('#list_page').live('pageinit',function(){

  $("#form_add_need").submit(function(e){

    hide_all('list_page');

    $.ajax({
      type:'POST',
      url:$(this).attr('action'),
      data:$(this).serialize(),
      crossDomain:true,
      success:function(data){
        retorno = JSON.parse(data);

        if (retorno.status == 'OK'){
          var nombre_need = $('#form_add_need').find('input[name="descripcion"]').val();
          var tipo_need = $('#form_add_need').find('input[name="tipo"]').val();
          var nuevo_need = {'descripcion': nombre_need, 'tipo': tipo_need};
          
          USUARIO.needs.push(nuevo_need);
          agregar_need_dom(nuevo_need);

        } else if (retorno.mensaje){
          show_alert(retorno.mensaje, 'list_page', 'error');
        } else if (retorno.form_errors) {
          show_form_errors(retorno.form_errors, 'list_page');
        }
      }
    });

    return false;
  });
});

$('document').ready(function(){
  if(!localStorage || !navigator.geolocation) {
    alert('Su dispositivo debe ser soportar Geolocalización y Almacenamiento Local HTML5');
    return;
  }

  if(!localStorage.getItem('distancia')) {
    localStorage.setItem('distancia', '100');
  }

  $('div.alert a.close').click(function(e){
    e.preventDefault();
    $(this).parents('.alert').css('display', 'none');
  })

  $('#form_login, #form_register').submit(function(){
    page_name = $(this).parents('div[data-role="page"]').attr('id');
    hide_all(page_name);

    $.ajax({
      type:'POST',
      url:$(this).attr('action'),
      data:$(this).serialize(),
      crossDomain:true,
      success:function(data){
        retorno = JSON.parse(data);

        if(retorno.status == 'OK'){
          USUARIO = retorno.usuario;
          localStorage.setItem('matches', JSON.stringify([]));
          window.location.href = '#list_page';

        } else if (retorno.mensaje) {
          show_alert(retorno.mensaje, page_name, 'error');

        } else if (retorno.form_errors) {
          show_form_errors(retorno.form_errors, page_name);
        }
      }
    });
    return false;
  });

});


function mostrar_form_add_need(){
  //alert($("#form_add_need").css('display'));
  $("#form_add_need").css('display','block');
}
function esconder_form_add_need(){
  $("#form_add_need").css('display','none');
}
function logout(){
  USUARIO = null;
  localStorage.removeItem('matches');
  $('#lista_needs').html('');
}


function actualizar_num_matches_listview(mis_matches) {
  $('#lista_needs li a').each(function(indice){

    var descripcion = $(this).find('span.descripcion').text();
    var num_matches = 0;

    for(var i=0 ; i<mis_matches.length ; ++i){
      if (mis_matches[i]['need_consultor_descripcion'] == descripcion) {
        num_matches += 1;
      }
    }

    $(this).find('span.ui-li-count').html(num_matches + "");
  })
}

/**
 * [Actualiza matches dentro del localStorage]
 * @param  {[list(match)} matches_recibidos [Matches recibidos por el servidor]
 * @return {[void]}
 */
function actualizar_matches(matches_recibidos){
  mis_matches = JSON.parse(localStorage.getItem('matches'));
  nuevos_matches = [];

  for(var i=0; i<matches_recibidos.length; ++i){
    var ya_estaba = false;

    for(var j=0; j<mis_matches.length; ++j){

      if (matches_recibidos[i]['need_consultado_descripcion'] == mis_matches[j]['need_consultado_descripcion']
        && matches_recibidos[i]['email_consultado'] == mis_matches[j]['email_consultado']){

        ya_estaba = true;
        break;
      }
    }

    if (!ya_estaba) {
      nuevos_matches.push(matches_recibidos[i]);
    }
  }

  mis_matches = mis_matches.concat(nuevos_matches);

  if (nuevos_matches.length !== 0) {
    // caso en que haya uno o mas matches nuevos
    actualizar_num_matches_listview(mis_matches);
    show_alert('Nuevo Match con Usuario', 'list_page', 'success');
    show_alert('Nuevo Match con Usuario', 'need_page', 'success');

  }

  localStorage.setItem('matches', JSON.stringify(mis_matches));
}


function get_matches(){
  if (USUARIO == null) {
    return;
  }

  var distancia = localStorage.getItem('distancia');
  var email = USUARIO.email;

  navigator.geolocation.getCurrentPosition(
    function(position){
      $.ajax({
        type:'POST',
        url: baseDir+'matches/',
        data:{
          'email': email,
          'distance': distancia,
          'latitude': position.coords.latitude,
          'longitude': position.coords.longitude,
          'app_id': '12'
        },
        crossDomain:true,
        success:function(data){
          var retorno = JSON.parse(data);
          actualizar_matches(retorno.matches);
        }
      });
    },
    function(error){
      console.log(error);
    }
  );
    

}

window.setInterval(function() { get_matches() }, 5000);
