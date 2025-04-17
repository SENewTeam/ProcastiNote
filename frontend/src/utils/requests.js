// frontend/src/utils/requests.js

const graphApi    = "http://localhost:8000/api/graph";
const searchApi   = "http://localhost:8000/api/search";
const userApi     = "http://localhost:8000/api/user";
const featuresApi = "http://localhost:8000/api/features";
const alertApi    = "http://localhost:8000/api/alert";
const commentsApi = "http://127.0.0.1:8000/api/comments";

// Generic JSON request wrapper
const performJsonRequest = (url, method, body = null, isAuth = false) => {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json" };
  if (isAuth) headers.Authorization = `Bearer ${token}`;

  return fetch(url, {
    method,
    headers,
    body: method === "GET" || !body ? null : JSON.stringify(body),
  })
    .then(async response => {
      if (response.status === 401 && isAuth) {
        localStorage.removeItem("token");
        window.location.href = "/login";
        return;
      }
      if (response.ok) return response.json();
      const err = await response.json().catch(() => null);
      return Promise.reject(err || { detail: `Request failed with status ${response.status}` });
    });
};

export class GraphApi {
  static getDetails(paperId) {
    return performJsonRequest(`${graphApi}/details?id=${paperId}`, "GET");
  }
  static getReferences(paperId) {
    return performJsonRequest(`${graphApi}/references?id=${paperId}`, "GET");
  }
  static getCitations(paperId) {
    return performJsonRequest(`${graphApi}/citations?id=${paperId}`, "GET");
  }
  static getRecommendations(paperId) {
    return performJsonRequest(`${graphApi}/recommendations?id=${paperId}`, "GET");
  }
  static getAuthorPapers(authorId) {
    return performJsonRequest(`${graphApi}/author_papers?id=${authorId}`, "GET");
  }
}

export class SearchApi {
  static search(query) {
    return performJsonRequest(`${searchApi}/completions?query=${encodeURIComponent(query)}`, "GET", null, true);
  }
}

export class UserApi {
  // Add a paper to user's history and fetch its details
  static getPaper(paperId) {
    const id = localStorage.getItem("id");
    return performJsonRequest(
      `${userApi}/${id}/papers/${paperId}/`,
      "POST",
      {},
      true
    );
  }

  // Fetch 5 most-recently read papers
  static getPapers() {
    const id = localStorage.getItem("id");
    return performJsonRequest(
      `${userApi}/${id}/papers`,
      "GET",
      null,
      true
    );
  }

  // Fetch all papers for filter dropdowns
  static getAllPapers() {
    const id = localStorage.getItem("id");
    return performJsonRequest(
      `${userApi}/${id}/papers/all`,
      "GET",
      null,
      true
    );
  }

  // Fetch filtered papers (OR logic)
  static filterPapers(filters) {
    const id = localStorage.getItem("id");
    const qs = new URLSearchParams(filters).toString();
    return performJsonRequest(
      `${userApi}/${id}/papers/filtered?${qs}`,
      "GET",
      null,
      true
    );
  }

  // Authentication endpoints
  static login({ email, password }) {
    return performJsonRequest(
      `${userApi}/login`,
      "POST",
      { email, password }
    );
  }

  static register({ username, email, password, profile }) {
    return performJsonRequest(
      `${userApi}/register`,
      "POST",
      { username, email, password, profile }
    );
  }

  static info() {
    return performJsonRequest(
      `${userApi}/info`,
      "GET",
      null,
      true
    );
  }

  static getRecommendations() {
    return performJsonRequest(
      `${userApi}/recommendations`,
      "GET",
      null,
      true
    );
  }
}

export class FeaturesApi {
  static aiRewrite(text) {
    return performJsonRequest(
      `${featuresApi}/ai/rewrite`,
      "POST",
      { text },
      true
    );
  }

  static conferences() {
    return performJsonRequest(
      `${featuresApi}/conferences`,
      "GET",
      null,
      true
    );
  }
}

export class AlertApi {
  static getAlert({ user, keyword, paperId }) {
    return performJsonRequest(
      `${alertApi}/getalert`,
      "POST",
      { user, keyword, paperId },
      true
    );
  }
}

export class CommentsApi {
  static create({ paper_id, user, text, keyword }) {
    return performJsonRequest(
      `${commentsApi}/create/`,
      "POST",
      { paper_id, user, text, keyword },
      true
    );
  }

  static update(commentId, { paper_id, user, text, keyword }) {
    return performJsonRequest(
      `${commentsApi}/updateComment/${commentId}/`,
      "PUT",
      { paper_id, user, text, keyword },
      true
    );
  }

  static getAllComment() {
    return performJsonRequest(
      `${commentsApi}/getAllComment/`,
      "POST",
      { user: localStorage.getItem("username") },
      true
    );
  }

  static deleteComment(commentId) {
    return performJsonRequest(
      `${commentsApi}/deleteComment/${commentId}/`,
      "DELETE",
      null,
      true
    );
  }
}
