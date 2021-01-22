Vue.component('courses', {
	template: `
	<div class="secondary-main">
		<nav class="secondary-nav">
		    <label class="filter-input">Passées<input type="checkbox" v-model="show_only_finished" /></label>
		    <label class="filter-input">Suivies<input type="checkbox" v-model="show_only_started" /></label>
			<ul v-for="(slot_courses, slot) in sorted_courses">
				<h3>Créneau {{ slot }}</h3>
				<li v-for="course in slot_courses">
					<input type="radio" :id="course.id" :value="course.id" v-model="selected_course" class="navbar-selection">
					<label :for="course.id" class="navbar-selection">{{ course.code }}</label>
				</li>
			</ul>
		</nav>
		<div class="div-margin">
			<course-details :id="selected_course"/>
		</div>
	</div>
	`,
	data: function() {
		return {
			courses: [],
			selected_course: undefined,
			show_only_finished: false,
			show_only_started: true
		}
	},
	computed: {
	    sorted_courses() {
	        let sorted_courses = {};
	        for (const course of this.courses) {
	            if (this.show_only_finished && !course.done) continue;
	            if (this.show_only_started && !(course.in_progress || course.done)) continue;
	            if (!sorted_courses[course.slot]) sorted_courses[course.slot] = [];
	            let copied_course = {...course}; // Deep copy
	            delete copied_course.slot;
	            sorted_courses[course.slot].push(copied_course);
	        }
	        return sorted_courses;
	    }
	},
	methods: {
		async searchCourses() {
			const response = await fetch(`/back/ue_list`);
			this.info = await response.json();
			for (let i = 0; i < this.info.length; i++) {
				const info_course = this.info[i];
				const new_course = {
					id: info_course.id,
				    code: info_course.code,
				    slot: info_course.creneau,
				    in_progress: info_course.en_cours,
				    done: info_course.termine
				};
				const course_index = this.courses.findIndex(c => c.code == info_course.code);
				if (course_index > -1) Vue.set(this.courses, course_index, new_course);
				else this.courses.push(new_course);			
			}
		}
	},
	mounted: function() {
		this.searchCourses();
	},
})

Vue.component('course-details', {
	props: ["id"],
	template: `
	<div>
		<h1>{{ code }} - {{ name }}</h1>
		<h3>Description :</h3>
		<p>{{ description }}</p>
		<h3>Responsable : <span class="normal">{{ teacher }}</span></h3>
		<table id="course-details-table">
			<tbody>
				<tr>
					<td>Période : {{ period }}</td>
					<td>Grade : {{ grade }}</td>
					<td>
						<tr>Jetons : {{ tokens }}</tr>
						<tr>ECTS : {{ ects[0] }}/{{ ects[1] }}</tr>
					</td>
				</tr>
			</tbody>
		</table>
		<course-table :skills="skills" @clicked="updateTokens" />
	</div>
	`,
	data: function() {
		return {
			name: "",
			code: "",
			description: "",
			teacher: "",
			period: "",
			grade: "",
			tokens: 0,
			ects: [0,0],
			skills: []
		}
	},
	methods: {
		async searchDetails() {
			let id = this.id;
			if (this.id === undefined) id = 3;
			const response = await fetch(`/back/ue/${id}`);
			this.info = await response.json();
			this.code = this.info.code;
			this.name = this.info.nom;
			this.description = this.info.description;
			this.teacher = this.info.responsable;
			this.period = this.info.periode;
			this.grade = this.info.grade;
			if (this.info.suivi == true) {
				this.ects[0] = Math.max(0, this.info.ects_obtenus);
				this.ects[1] = Math.max(0, this.info.ects_tentes);
				this.skills = [];
				for (var i = 0; i < this.info.competences.length; i++) {
					this.skills.push(this.info.competences[i]);
				}
			}			
		},
		updateTokens(result) {
			this.tokens = result;
		}
	},
	mounted: function() {
		this.searchDetails();
	},
	watch: {
		id() {
			this.searchDetails();
		}
	}
})

Vue.component('course-table', {
	props: ["skills"],
	template: `
	<div>
		<table id="course-skills-table" class="info-table">
			<thead>
				<th>Compétence</th>
				<th>Niveau</th>
				<th>Jetons</th>
				<th>Evaluation</th>
			</thead>
			<tbody v-for="row in details">
				<tr>
					<td>{{ row.name }}</td>
					<td>{{ row.level }}</td>
					<td>{{ row.tokens[0] }}/{{ row.tokens[1] }}</td>
					<td>{{ row.eval }}</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	data: function() {
		return {
			details: [],
			tokens_total: 0
		}
	},
	methods: {
		async searchDetails() {
			this.details.splice(0);
			this.tokens_total = 0;
			for (var i = 0; i < this.skills.length; i++) {
				let id = this.skills[i];
				const response = await fetch(`/back/comp_eval/${id}`);
				this.info = await response.json();
				let course = {
					name: this.info.competence,
					level: this.info.niveau,
					eval: this.info.note,
					tokens: [this.info.jetons_valides, this.info.jetons_tentes]
				}
				this.tokens_total += course.tokens[0];
				Vue.set(this.details, i, course);
			}
			this.$emit('clicked', this.tokens_total);
		}
	},
	mounted: function() {
		this.searchDetails();
	},
	watch: {
		skills() {
			this.searchDetails();
		}
	}
})
