Vue.component('courses', {
	template: `
	<div class="div-margin">
		<nav class="nav-two">
			<div>
			    <label>Passées<input type="checkbox" v-model="show_only_finished" /></label>
			    <label>Suivies<input type="checkbox" v-model="show_only_started" /></label>
				<ul v-for="(slot_courses, slot) in sorted_courses">
					<li><h3>Créneau {{ slot }}</h3></li>
					<ul v-for="course in slot_courses">
						<li>
							<input type="radio" :id="course.id" :value="course.id" v-model="selected_course" class="navbar-selection">
							<label :for="course.id" class="navbar-selection">{{ course.code }}</label>
						</li>
					</ul>
				</ul>
			</div>
		</nav>
		<div style="margin-left: 200px;">
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
						<tr>ECTS : {{ ects }}</tr>
					</td>
				</tr>
			</tbody>
		</table>
		<course-table />
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
			tokens: "",
			ects: ""
		}
	},
	methods: {
		async searchDetails() {
			const response = await fetch(`/back/ue/${this.id}`);
			this.info = await response.json();
			this.code = this.info.code;
			this.name = this.info.nom;
			this.description = this.info.description;
			this.teacher = this.info.responsable;
			this.period = this.info.periode;
			this.grade = this.info.grade;
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
	props: ["code"],
	template: `
	<div>
		<table id="course-skills-table" class="info-table">
			<thead>
				<th>Compétence</th>
				<th>Niveau</th>
				<th>Jetons</th>
				<th>Evaluation</th>
			</thead>
			<tbody v-for="row in details.skills">
				<tr>
					<td>{{ row.name }}</td>
					<td>{{ row.level }}</td>
					<td>{{ row.tokens }}</td>
					<td>{{ row.eval }}</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	methods: {
		searchDetails() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			this.details = {
				period: 'A2S2',
				grade: 'C',
				tokens: '3/3',
				ects: '4/5',
				skills: [
					{
						name : 'CSG1',
						level : '3',
						tokens: '3',
						eval: '='
					},
					{
						name : 'CSG3',
						level : '3',
						tokens: '3',
						eval: '+'
					},
					{
						name : 'CST1',
						level : '2',
						tokens: '3',
						eval: '='
					}
				]
			}		
		}	
	},
	created: function() {
		this.searchDetails();
	}
})
