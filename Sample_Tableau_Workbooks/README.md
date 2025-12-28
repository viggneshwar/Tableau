📖 Tableau Dashboard Design Standards
This repository includes a Dashboard Design Checklist to ensure every Tableau dashboard meets enterprise best practices. The checklist helps developers, analysts, and designers validate dashboards before release.

⚙️ Tableau Dashboard Technical Checklist
🔧 Data Connections
- [ ] Prefer extracts over live connections for better performance and stability
- [ ] Use incremental refresh where possible to reduce load times
- [ ] Remove unused tables, fields, and joins from data sources
- [ ] Ensure data sources are published and governed centrally
🧮 Calculations
- [ ] Avoid overly complex calculations inside Tableau (push logic to the database/ETL if possible)
- [ ] Reuse calculated fields instead of duplicating logic
- [ ] Document calculation formulas for transparency
- [ ] Test calculations for accuracy and performance impact
⚡ Performance Optimization
- [ ] Limit the number of filters and quick filters
- [ ] Use context filters wisely to improve query speed
- [ ] Minimize use of high‑cardinality filters (e.g., customer IDs)
- [ ] Aggregate data before bringing it into Tableau when possible
📊 Workbook & Dashboard Efficiency
- [ ] Remove unused worksheets, fields, and parameters
- [ ] Optimize workbook size by cleaning up hidden fields
- [ ] Use fixed axis ranges to avoid unnecessary recalculations
- [ ] Test dashboard load time and optimize queries before publishing
🛡️ Governance & Maintenance
- [ ] Follow naming conventions for datasources, fields, and workbooks
- [ ] Apply row‑level security and permissions consistently
- [ ] Document data sources, refresh schedules, and dependencies
- [ ] Regularly review extract refresh frequency vs. actual usage



📊 Tableau Dashboard Layout Template
This section provides a recommended wireframe for Tableau dashboards. Use it as a starting point to ensure dashboards are clean, consistent, and aligned with design standards.
🖼️ Wireframe Structure
- Top Section (KPIs) → Quick glance metrics for executives
- Middle Section (Trends) → Charts showing performance over time and comparisons
- Lower Section (Details) → Maps, tables, or drill‑downs for analysts
- Side/Bottom Section (Filters) → Interactive controls for exploration
- Footer (Insights) → Written context or recommendations
⚡ Usage Workflow
- Start with summary KPIs at the top
- Add trend charts in the middle for context
- Provide detailed breakdowns below for deeper analysis
- Place filters in a consistent location (top or side)
- End with insights or recommendations to guide decisions
