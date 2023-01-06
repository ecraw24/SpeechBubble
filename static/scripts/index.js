addEventListener("DOMContentLoaded", function() {
    var commandButtons = document.querySelectorAll(".button-15, .buttonImage");
    var speechDisplay = document.querySelector(".speechDisplayText");
    
    var grid = document.getElementById('board');
    grid.style.setProperty('--cols', Math.ceil(Math.sqrt(grid.children.length))*2);
    grid.style.setProperty('--rows', Math.ceil(Math.sqrt(grid.children.length)));
    console.log(Math.ceil(Math.sqrt(grid.children.length)));
    
    for (var i=0, l=commandButtons.length; i<l; i++) {
      var button = commandButtons[i];
      button.addEventListener("click", function(e) {
        e.preventDefault();
        var clickedButton = e.target;
        var command = clickedButton.value; 
        var request = new XMLHttpRequest();
        request.open("GET", "/?command=" + command + "&gender=" + document.getElementById("submitGender").value, true);
        request.send();
        speechDisplay.innerHTML=command; 
      });
    }
  
    recordButton = document.querySelector("#record"); 
    recordButton.addEventListener("click", function(){
      var counter = 15;
      //recordButton.disabled = true; 
      setInterval(function() {
          counter--;
          span = document.querySelector("#countdown");
          if (counter >= 0) {
            span.innerHTML = counter;
          }
          if (counter === 0) {
            clearInterval(counter);
            span.innerHTML = "--"; 
          }
        }, 1000); 
    });
  }, true);

  function openParameters() {
    document.getElementById("parameters").style.display = "block";
    document.getElementById("board").style.pointerEvents = "none";
    document.getElementById("board").style.backdropFilter = "blur(10px)";
    document.getElementById("record").style.pointerEvents = "none";
    document.getElementById("record").style.backdropFilter = "blur(10px)";

  }
  
  function closeParameters() {
    saveCurrentParameters(); 
    document.getElementById("parameters").style.display = "none";
    document.getElementById("board").style.pointerEvents = "auto";
    document.getElementById("board").style.backdropFilter = "none";
    document.getElementById("record").style.pointerEvents = "auto";
    document.getElementById("record").style.backdropFilter = "none";
  }

  function saveCurrentParameters() {
      document.getElementById("submitMaxButtons").value=document.getElementById("maxButtons").value;
      document.getElementById("submitGradeLevel").value=document.getElementById("gradeLevel").value;
      document.getElementById("submitGender").value=document.querySelector('input[name="gender"]:checked').value;
      document.getElementById("submitExtractionType").value=document.querySelector('input[name="extraction"]:checked').value;
      console.log(document.getElementById("submitGender").value)
  }

  function toggleGradeLevel() {
    if (document.getElementById("autoGradeLevel").checked || document.getElementById("verbatim").checked) {
      document.getElementById("gradeLevel").value='0'; 
      document.getElementById("gradeLevel").disabled=true; 
    } else {
      document.getElementById("gradeLevel").disabled=false; 
    }
  }


