(function(){
  var root=document.documentElement, fs=1.06, min=0.9, max=1.5;
  function apply(){root.style.setProperty('--fs',fs.toFixed(3)+'rem');}
  document.getElementById('tplus').onclick=function(){fs=Math.min(max,fs+0.08);apply();};
  document.getElementById('tminus').onclick=function(){fs=Math.max(min,fs-0.08);apply();};
  document.getElementById('treset').onclick=function(){fs=1.06;apply();};
  document.getElementById('hc').onclick=function(){root.classList.toggle('hc');};

  // ---- Live deadline countdowns ----
  var DAY=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  function today(){ var n=new Date(); return new Date(n.getFullYear(),n.getMonth(),n.getDate()); }
  function daysUntil(iso){
    var p=iso.split('-'); var d=new Date(+p[0],+p[1]-1,+p[2]);
    return Math.round((d - today())/86400000);
  }
  function wordN(n){ var w=['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen']; return n<w.length?w[n]:String(n); }
  document.querySelectorAll('.deadrow[data-deadline]').forEach(function(row){
    var d=daysUntil(row.getAttribute('data-deadline'));
    var chip=row.querySelector('.cd'); if(!chip) return;
    var cls,txt;
    if(d<0){cls='cd-closed';txt='Closed';row.classList.add('is-closed');}
    else if(d===0){cls='cd-now';txt='Closes today';}
    else if(d===1){cls='cd-now';txt='Closes tomorrow';}
    else if(d<=3){cls='cd-soon';txt='In '+wordN(d)+' days';}
    else if(d<=10){cls='cd-mid';txt='In '+wordN(d)+' days';}
    else {cls='cd-far';txt='In '+wordN(d)+' days';}
    chip.className='cd '+cls; chip.textContent=txt;
  });

  // ---- Interactive reach-out checklist ----
  var list=document.getElementById('reachList');
  var prog=document.getElementById('checkProg');
  function refreshProg(){
    if(!list||!prog) return;
    var items=list.querySelectorAll('li');
    var done=list.querySelectorAll('li.done').length;
    var left=items.length-done;
    prog.textContent = done===0
      ? 'None checked off yet, '+wordN(items.length)+' to go'
      : (left===0 ? 'All done, nice work' : wordN(done)+' done, '+wordN(left)+' to go');
  }
  function toggle(li){ li.classList.toggle('done'); li.setAttribute('aria-checked', li.classList.contains('done')?'true':'false'); refreshProg(); }
  if(list){
    list.querySelectorAll('li').forEach(function(li){
      li.addEventListener('click',function(){toggle(li);});
      li.addEventListener('keydown',function(e){ if(e.key===' '||e.key==='Enter'){e.preventDefault();toggle(li);} });
    });
    refreshProg();
  }

  // ---- Match table filter + sort ----
  var rows=Array.prototype.slice.call(document.querySelectorAll('.matchtable tbody tr[data-score]'));
  var chips=document.querySelectorAll('.controls .chip[data-geo]');
  var condOnly=document.getElementById('condOnly');
  var sortToggle=document.getElementById('sortToggle');
  var countEl=document.getElementById('matchCount');
  var detailsEl=document.querySelector('#matches details');
  var curGeo='all', desc=true;

  function bodyOf(r){ return r.parentNode; }
  function applyFilter(){
    var shown=0;
    rows.forEach(function(r){
      var ok = (curGeo==='all' || r.getAttribute('data-geo')===curGeo)
            && (!condOnly.checked || r.getAttribute('data-read')==='conditional');
      r.classList.toggle('hidden-row', !ok);
      if(ok) shown++;
    });
    // sort within each tbody
    var bodies=new Set(rows.map(bodyOf));
    bodies.forEach(function(tb){
      var rs=Array.prototype.slice.call(tb.querySelectorAll('tr[data-score]'));
      rs.sort(function(a,b){ var d=(+a.getAttribute('data-score'))-(+b.getAttribute('data-score')); return desc?-d:d; });
      rs.forEach(function(r){ tb.appendChild(r); });
    });
    if(countEl) countEl.textContent = shown===rows.length ? ('Showing all '+wordN(rows.length)+' matches') : ('Showing '+wordN(shown)+' of '+wordN(rows.length));
    if(detailsEl && (curGeo!=='all' || condOnly.checked)) detailsEl.open=true;
  }
  chips.forEach(function(c){
    c.addEventListener('click',function(){
      chips.forEach(function(x){x.classList.remove('active');});
      c.classList.add('active'); curGeo=c.getAttribute('data-geo'); applyFilter();
    });
  });
  if(condOnly) condOnly.addEventListener('change',applyFilter);
  if(sortToggle) sortToggle.addEventListener('click',function(){
    desc=!desc; sortToggle.textContent = desc?'Sort: highest score':'Sort: lowest score'; applyFilter();
  });
  applyFilter();
})();