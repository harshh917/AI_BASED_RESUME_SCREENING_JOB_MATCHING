import api from './api'

export async function uploadResume(file) {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post('/api/resumes/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function listResumes() {
  const { data } = await api.get('/api/resumes')
  return data
}

export async function getResume(id) {
  const { data } = await api.get(`/api/resumes/${id}`)
  return data
}

export function getResumeFileUrl(id) {
  const base = api.defaults.baseURL || ""
  return `${base}/api/resumes/${id}/file`
}

export async function viewResume(id) {
  const response = await api.get(`/api/resumes/${id}/file`, { responseType: "blob" })
  const blobUrl = URL.createObjectURL(response.data)
  window.open(blobUrl, "_blank", "noopener,noreferrer")
  setTimeout(() => URL.revokeObjectURL(blobUrl), 60_000)
}

export async function createJob({ title, description }) {
  const { data } = await api.post('/api/jobs', { title, description })
  return data
}

export async function listJobs() {
  const { data } = await api.get('/api/jobs')
  return data
}

export async function getJob(id) {
  const { data } = await api.get(`/api/jobs/${id}`)
  return data
}

export async function deleteJob(id) {
  await api.delete(`/api/jobs/${id}`)
}

export async function runMatchingForJob(jobId) {
  const { data } = await api.post(`/api/matching/job/${jobId}/run`)
  return data
}

export async function getRankedResults(jobId) {
  const { data } = await api.get(`/api/matching/${jobId}/results`)
  return data
}

export async function getMatchDetail(jobId, resumeId) {
  const { data } = await api.get(`/api/matching/${jobId}/${resumeId}`)
  return data
}

export async function updateJob(id, payload) {
  const { data } = await api.put(`/api/jobs/${id}`, payload)
  return data
}

export async function getJobStats(id) {
  const { data } = await api.get(`/api/jobs/stats/${id}`)
  return data
}

export async function getRecommendedJobs() {
  const { data } = await api.get('/api/recommendations/jobs')
  return data
}
