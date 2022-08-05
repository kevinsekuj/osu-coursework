// You are not permitted to change this in any way
function Student(name, major, yearInSchool, club) {
	this.name = name; // string, (e.g. "Jim", "Pam", "Michael")
	this.major = major; // string, (e.g. "Computer Science", "Art", "Business")
	this.yearInSchool = yearInSchool; // int, (e.g. 1, 2, 3, 4)
	this.club = club; // string, (e.g. "Improv", "Art")
}

var students = [
	new Student("Pam", "Art", 2, "Art"),
	new Student("Michael", "Business", 4, "Improv"),
	new Student("Dwight", "Horticulture", 1, "Karate"),
	new Student("Jim", "Sports Science", 2, "Guitar"),
	new Student("Angela", "Accounting", 4, "Cat"),
	new Student("Toby", "Human Resources", 3, "Photography"),
];

// create new prototype method available on all Student instances
Student.prototype.logMe = function (club) {
	if (club) {
		console.log(
			`${this.name} - ${this.major} - ${this.yearInSchool} - ${this.club}`
		);
	} else {
		console.log(`${this.name} - ${this.major} - ${this.yearInSchool}`);
	}
};

/* This function sorts arrays using an arbitrary comparator. You pass it a comparator 
  and an array of objects appropriate for that comparator and it will return a new array 
  which is sorted with the largest object in index 0 and the smallest in the last index*/

function sortArr(comparator, array) {
	// bubble sort implementation
	for (let i = 0; i < array.length - 1; i++) {
		for (let j = 0; j < array.length - i - 1; j++) {
			if (comparator(array[j], array[j + 1])) {
				let temp = array[j];
				array[j] = array[j + 1];
				array[j + 1] = temp;
			}
		}
	}
	return array;
}

/* A comparator takes two arguments and uses some algorithm to compare them. If the first 
  argument is larger or greater than the 2nd it returns true, otherwise it returns false.
  Here is an example that works on integers*/
function exComparator(int1, int2) {
	if (int1 > int2) {
		return true;
	} else {
		return false;
	}
}

/* For all comparators if students are 'tied' according to the comparison rules then the order of 
  those 'tied' students is not specified and either can come first*/

/* This compares two students based on their year in school. Sort in descending order.*/
function yearComparator(student1, student2) {
	if (student1.yearInSchool < student2.yearInSchool) {
		return true;
	}
	return false;
}

/* This compares two students based on their major. It should be case insensitive and 
  makes which are alphabetically earlier in the alphabet are "greater" than ones that 
  come later (from A-Z).*/
function majorComparator(student1, student2) {
	if (student1.major.toLowerCase() > student2.major.toLowerCase()) {
		return true;
	}
	return false;
}

/* This compares two students based on the club they're in. The ordering from "greatest" 
  to "least" is as follows: improv, cat, art, guitar, (types not otherwise listed). 
  It should be case insensitive. If two clubs are of equal type then the student who
  has the higher year in school should be "greater."*/

function clubComparator(student1, student2) {
	const clubs = {
		improv: 4,
		cat: 3,
		art: 2,
		guitar: 1,
	};
	const year1 = student1.yearInSchool;
	const year2 = student2.yearInSchool;

	if (student1.club.toLowerCase() in clubs) {
		var club1 = clubs[student1.club.toLowerCase()];
	} else {
		var club1 = 0;
	}
	if (student2.club.toLowerCase() in clubs) {
		var club2 = clubs[student2.club.toLowerCase()];
	} else {
		var club2 = 0;
	}

	if (club1 === club2) {
		if (year1 < year2) {
			return true;
		}
		return false;
	}
	if (club1 < club2) {
		return true;
	}

	return false;
}

const year = sortArr(yearComparator, students);

console.log("**********");
console.log("The students sorted by year in school are:");
year.forEach(element => {
	element.logMe();
});

console.log("");

const major = sortArr(majorComparator, students);

console.log("**********");
console.log("The students sorted by major are:");
major.forEach(element => {
	element.logMe();
});

console.log("");

const clubs = sortArr(clubComparator, students);

console.log("**********");
console.log("The students sorted by club affiliation are:");
clubs.forEach(element => {
	element.logMe(true);
});

console.log("");
console.log("**********");
