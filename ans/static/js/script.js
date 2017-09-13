av=[1,1,1,1,1] ; // availabilty of questions for each stadium 1:available 0:not available
left=[0.13,0.31,0.52,0.72,0.93];  // left constraint for popup visibility
right=[0.17,0.36,0.56,0.77,0.97];  // right constraint for popup visibility
(function($)
 {
        $.jInvertScroll(['.scroll'],        // an array containing the selector(s) for the elements you want to animate
        {
		height: 'auto',
	        width: 'auto',
// optional: define the height the user can scroll, otherwise the overall length will be taken as scrollable height
	        onScroll: function(percent)
		{  
//optional: callback function that will be called when the user scrolls down, useful for animating other things on the page
              console.log(percent);
			for(i=0;i<5;i++)
			{
		        if (percent>left[i]&&percent<right[i]) 
				{
			        if (av[i]==1)
	                        document.getElementById("Available"+String(i+1)).style.display='block';
		                else 
		                document.getElementById("NotAvailable"+String(i+1)).style.display='block';
		            
		                } 
			else
		 	{
		        document.getElementById("Available"+String(i+1)).style.display='none';
		        document.getElementById("NotAvailable"+String(i+1)).style.display='none';
		        }   
			}
                 }
           });
}(jQuery));
    function dismissDiv() 
    {
	for(i=0;i<5;i++)
		{
        	document.getElementById('Quiz'+String(i+1)).style.display='none';
		}
        document.getElementById('instructionsDiv').style.display='none';
        document.getElementById('leaderboardDiv').style.display='none';
        enable_scroll();
    }
    function displayQuiz(x) {
        document.getElementById('Quiz'+String(x+1)).style.display='block';
        document.getElementById('Available'+String(x+1)).style.display='none';
        disable_scroll();
    }
    function dismissPopUp(a) {
        document.getElementById('Available'+String(a+1)).style.display='none';
        document.getElementById('NotAvailable'+String(a+1)).style.display='none';
    }
    function openInstructions() {
    dismissDiv();
    document.getElementById('instructionsDiv').style.display='block';
    disable_scroll();
    }
    function displayLeaderboard() {
    dismissDiv();
    disable_scroll();
    document.getElementById('leaderboardDiv').style.display='block';
    }
   
function disable_scroll(){
    document.getElementsByTagName("body")[0].style.overflowY="hidden";
}

function enable_scroll(){
    document.getElementsByTagName("body")[0].style.overflowY="visible";
}

window.onbeforeunload= function()
{
	window.scrollTo(0,0);
}
