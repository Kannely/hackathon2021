const app = new Vue({
    el: '#app',
	delimiters: ["[[", "]]"],
    data: {
	    favoriteCat: 'Berlioz'
    },
    computed: {
	    label() {
		    return 'New favorite cat : ' + this.favoriteCat
	    }
    },
    methods: {
	    alertCat(catName) {
		    alert('My favorite cat is ' + catName);
	    },
	    changeCat() {
		    this.favoriteCat = 'Garfield';
		    this.alertCat(this.favoriteCat)
	    }
	}
})
// TODO : Change
