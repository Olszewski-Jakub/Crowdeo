/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure

  // But you can create a sidebar manually

  pandaSidebar: [
    {
      type: "category",
      label: "Panda",
      items: ["panda/intro"],
    },
  ],
  bambooSidebar: [
    {
      type: "category",
      label: "Bamboo",
      items: [
        {
          type: "category",
          label: "Project Overview",
          items: [
            "bamboo/projectOverview/main_features",
            "bamboo/projectOverview/installation_steps",
            "bamboo/projectOverview/tech_stack",
            "bamboo/projectOverview/contribution_guidelines",
          ],
        },
        //Category includeing information about database
        {
          type: "category",
          label: "System Configuration and Authentication.",
          items: ["bamboo/database"],
        },
      ],
    },
  ],
  dashboardSidebar: [
    {
      type: "category",
      label: "CrowdeoDashboard",
      items: ["crowdeoDashboard/intro"],
    },
  ],
};

export default sidebars;
