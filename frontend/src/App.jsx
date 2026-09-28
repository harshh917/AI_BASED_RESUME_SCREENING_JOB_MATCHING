import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './hooks/useAuth'
import MainLayout from './layouts/MainLayout'
import ProtectedRoute from './components/ProtectedRoute'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import CandidateDashboard from './pages/CandidateDashboard'
import UploadResumePage from './pages/UploadResumePage'
import MyResumePage from './pages/MyResumePage'
import JobBrowsePage from './pages/JobBrowsePage'
import RecruiterDashboard from './pages/RecruiterDashboard'
import CreateJobPage from './pages/CreateJobPage'
import JobDetailsPage from './pages/JobDetailsPage'
import MatchDetailsPage from './pages/MatchDetailsPage'
import JobDetailsCandidatePage from './pages/JobDetailsCandidatePage'
import MyApplicationsPage from './pages/MyApplicationsPage'
import RecruiterApplicationsPage from './pages/RecruiterApplicationsPage'
import EditJobPage from './pages/EditJobPage'
import EvaluationPage from './pages/EvaluationPage'
import DataExplorerPage from './pages/DataExplorerPage'

const cand = (el) => <ProtectedRoute allowedRoles={['candidate', 'admin']}>{el}</ProtectedRoute>
const rec = (el) => <ProtectedRoute allowedRoles={['recruiter', 'admin']}>{el}</ProtectedRoute>

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <MainLayout>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/candidate" element={cand(<CandidateDashboard />)} />
            <Route path="/candidate/upload" element={cand(<UploadResumePage />)} />
            <Route path="/candidate/resume" element={cand(<MyResumePage />)} />
            <Route path="/candidate/jobs" element={cand(<JobBrowsePage />)} />
            <Route path="/candidate/jobs/:jobId" element={cand(<JobDetailsCandidatePage />)} />
            <Route path="/candidate/applications" element={cand(<MyApplicationsPage />)} />
            <Route path="/recruiter" element={rec(<RecruiterDashboard />)} />
            <Route path="/recruiter/evaluation" element={rec(<EvaluationPage />)} />
            <Route path="/recruiter/data" element={rec(<DataExplorerPage />)} />
            <Route path="/recruiter/jobs/new" element={rec(<CreateJobPage />)} />
            <Route path="/recruiter/jobs/:jobId/edit" element={rec(<EditJobPage />)} />
            <Route path="/recruiter/jobs/:jobId" element={rec(<JobDetailsPage />)} />
            <Route path="/recruiter/jobs/:jobId/candidates/:resumeId" element={rec(<MatchDetailsPage />)} />
            <Route path="/recruiter/jobs/:jobId/applications" element={rec(<RecruiterApplicationsPage />)} />
          </Routes>
        </MainLayout>
      </BrowserRouter>
    </AuthProvider>
  )
}
