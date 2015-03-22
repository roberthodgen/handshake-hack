Parse.initialize("Aw2wgeVa9ihzU3OqRggicJ2rcFoQFxQYIWDhnaFR", "L9MiISVVsgSPcSSkJt67X8VMUqpcuuHADSG4lJpz");

function uploadResume() {
  var TestObject = Parse.Object.extend("TestObject");
  var testObject = new TestObject();
  testObject.save({foo: "bar"}).then(function(object) {
    alert("yay! it worked");
  });
}

function submitReq() {
  var userName = document.getElementById("username").value;
  if (!userName) {
    alert("Enter a proper username");
  } else {
    var JobSeeker = Parse.Object.extend("JobSeeker");
    var query = new Parse.Query(JobSeeker);
    query.equalTo("username", userName);
    query.find({
        success: function(results) {
            //update resume
            if (results.length == 0) {
              var JobSeeker = Parse.Object.extend("JobSeeker");
              var jobSeeker = new JobSeeker();
              console.log("Error, Problem");
              jobSeeker.save({username: userName}).then(function(object) {
                alert("Successfully uploaded your resume.");
              });
            } else {
              console.log("Success reached");
              alert("Successfully updated your resume." + results[0].get('username'));
            }
        },
        error: function(error) {
          alert("Unsuccessful connection");
        }
    });
  }
}
