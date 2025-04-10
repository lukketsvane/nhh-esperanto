# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands
- Install: `npm install --legacy-peer-deps` or `pnpm install --no-strict-peer-dependencies`
- Dev server: `npm run dev`
- Build: `npm run build`
- Start: `npm start`
- Lint: `npm run lint`

## Code Style Guidelines
- **TypeScript**: Use strict typing with defined interfaces for props and data structures
- **Imports**: Follow path alias pattern `@/*` for internal imports
- **Components**: Use functional components with React hooks
- **Naming**: camelCase for variables/functions, PascalCase for components/types
- **Error Handling**: Use try/catch with explicit error logging
- **Data Processing**: Handle null/undefined values explicitly
- **Formatting**: Follow existing indentation (2 spaces) and code organization
- **CSS**: Use Tailwind utility classes for styling
- **State Management**: Use React hooks like useState/useEffect/useMemo for local state