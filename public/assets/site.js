/* Shared behaviour for every page. Each block checks that its elements exist. */
(function(){
  var $=function(id){return document.getElementById(id)};

  /* mobile menu */
  var bg=$('burger'),mn=$('mnav');
  if(bg&&mn){
    bg.onclick=function(){var o=mn.hidden;mn.hidden=!o;bg.setAttribute('aria-expanded',o)};
    mn.addEventListener('click',function(e){if(e.target.tagName==='A'){mn.hidden=true;bg.setAttribute('aria-expanded','false')}});
  }

  /* marquees: duplicate content for a seamless loop */
  ['track','logos'].forEach(function(id){var el=$(id);if(el)el.innerHTML+=el.innerHTML});

  /* hero slider (home only) */
  var slides=[].slice.call(document.querySelectorAll('.slide')),hd=$('hero-dots');
  if(slides.length&&hd){
    var cur=0,timer,still=matchMedia('(prefers-reduced-motion: reduce)').matches;
    slides.forEach(function(s,i){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Slide '+(i+1));b.onclick=function(){go(i,true)};hd.appendChild(b)});
    var go=function(i,user){
      slides[cur].classList.remove('on');cur=(i+slides.length)%slides.length;slides[cur].classList.add('on');
      [].forEach.call(hd.children,function(d,j){d.setAttribute('aria-current',j===cur?'true':'false')});
      if(user)restart();
    };
    var restart=function(){clearInterval(timer);if(!still)timer=setInterval(function(){go(cur+1)},6000)};
    $('h-prev').onclick=function(){go(cur-1,true)};
    $('h-next').onclick=function(){go(cur+1,true)};
    go(0);restart();
  }

  /* scroll rails with dots */
  function dotsFor(sc,box){
    var cards=sc.children,dots=$(box);if(!cards.length||!dots)return;
    function per(){return Math.max(1,Math.round(sc.clientWidth/cards[0].offsetWidth))}
    function mark(){var w=cards[0].offsetWidth+24,idx=Math.round(sc.scrollLeft/w);[].forEach.call(dots.children,function(d,j){d.setAttribute('aria-current',j===Math.min(idx,dots.children.length-1)?'true':'false')})}
    function build(){
      var n=Math.max(1,cards.length-per()+1);dots.innerHTML='';
      for(var k=0;k<n;k++){(function(k){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Go to item '+(k+1));b.onclick=function(){sc.scrollTo({left:cards[k].offsetLeft-sc.offsetLeft,behavior:'smooth'})};dots.appendChild(b)})(k)}
      mark();
    }
    sc.addEventListener('scroll',mark,{passive:true});window.addEventListener('resize',build);build();
  }
  if($('prail'))dotsFor($('prail'),'pdots');
  if($('trail'))dotsFor($('trail'),'tdots');

  /* enquiry form: builds an email in the visitor's mail app */
  var f=$('enq'),st=$('e-status');
  if(f){
    var q=new URLSearchParams(location.search).get('product');
    if(q){[].forEach.call(f.product.options,function(o){if(o.value===q)f.product.value=q})}
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var n=f.name.value.trim(),m=f.message.value.trim();
      if(!n||!m){st.textContent='Add your name and a short scope so we can quote.';(n?f.message:f.name).focus();return}
      var body='Name: '+n+'\nCompany: '+f.company.value+'\nPhone: '+f.phone.value+'\nProduct: '+f.product.value+'\n\n'+m;
      location.href='mailto:sushant.hota@uniprofiles.in?subject='+encodeURIComponent('Enquiry: '+f.product.value)+'&body='+encodeURIComponent(body);
      st.textContent='Your email app should open with this enquiry filled in. If it does not, write to sushant.hota@uniprofiles.in and attach your drawings.';
    });
  }

  /* old one-page links (/#products etc.) land on the new pages */
  var old={'#about':'/about/','#products':'/products/','#projects':'/projects/','#clients':'/clients/','#testimonials':'/clients/#testimonials','#facility':'/facility/','#counters':'/about/#quality','#approvals':'/approvals/','#contact':'/contact/'};
  if((location.pathname==='/'||location.pathname==='/index.html')&&old[location.hash])location.replace(old[location.hash]);
})();
