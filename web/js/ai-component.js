Vue.component('ai-header', {
  data() {
    return {
      firstName: null,
      lastName: null
    }
  },
  created() {
    this.firstName = localStorage.getItem("firstName")
    this.lastName = localStorage.getItem("lastName")
  },
  template: `<div class="header-container">
              <div class="head-title"><slot></slot></div>
              <div class="head-info">
                <img src="image/avatar.png">
                <span>{{firstName}} {{lastName}}</span>
                <el-button type="text" style="margin-left: 10px" @click="logout">Logout</el-button>
              </div>
            </div>`,
  methods: {
    logout() {
      localStorage.clear()
      window.location.href = 'login.html'
    }
  }
});

Vue.component('ai-menu', {
  data() {
    return {}
  },
  props: {
    active: {
      type: String,
      default: ''
    }
  },
  created() {
  },
  template: `<el-menu :default-active="active" @select="handleSelect">
                <el-menu-item index="chat">
                  <i class="el-icon-chat-dot-round"></i>
                  <span slot="title">AI Chat</span>
                </el-menu-item>
                <el-menu-item index="courseList">
                  <i class="el-icon-edit-outline"></i>
                  <span slot="title">Course List</span>
                </el-menu-item>
                <el-menu-item index="addCourse">
                  <i class="el-icon-circle-plus-outline"></i>
                  <span slot="title">Add Course</span>
                </el-menu-item>
                <el-menu-item index="learningProgress">
                  <i class="el-icon-circle-plus-outline"></i>
                  <span slot="title">Learning Progress</span>
                </el-menu-item>
              </el-menu>`,
  methods: {
    handleSelect(key) {
      if (key === this.active) {
        return
      }
      window.location.href = key + '.html'
    },
  }
});

/**
 * @param routeName /runcode
 * @param dataJson {}
 * @returns {Promise<any>}
 */
function fetchPost(routeName, dataJson, method = 'POST') {
  return fetch('http://localhost:5500' + routeName, {
    method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataJson)
  }).then(response => response.json())
}

function fetchGet(routeName) {
  return fetch('http://localhost:5500' + routeName).then(response => response.json())
}
