import api from './api'

export async function applyToJob(jobId, payload) {
  const { data } = await api.post(`/api/applications/jobs/${jobId}`, payload)
  return data
}

export async function listMyApplications() {
  const { data } = await api.get('/api/applications/mine')
  return data
}

export async function listJobApplications(jobId) {
  const { data } = await api.get(`/api/applications/jobs/${jobId}`)
  return data
}

export async function updateApplicationStatus(applicationId, status) {
  const { data } = await api.patch(`/api/applications/${applicationId}/status`, { status })
  return data
}
