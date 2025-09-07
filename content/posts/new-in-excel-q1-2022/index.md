---
title: "What is new in Excel in Q1 2022"
summary: "This is when TEXTSPLIT appeared, a building block for working with LLMs in Excel."
date: 2022-04-24
categories: 
  - "Excel is All You Need"
  - "Blog"
tags: 
  - "Excel"
aliases: 
  - /blog/2022/04/24/what-is-new-in-excel-in-q1-2022/
---

Microsoft keeps adding new exciting features to Excel all the time. Here is an overview of new features added in the first quarter of 2022.

I base this on the Excel Blog. Please drop me a mail if I missed something. As Microsoft rolls out new features gradually, not everything might be available for you, right now.

For me, `TEXTSPLIT` is the best new Excel feature of this quarter. With it you can split text that is eg. formatted as CSV into multiple rows and columns. This is extremely helpful if you want to use ChatGPT in Excel.

## 3 New Excel Functions for Text Extraction

Three new functions make it easier to extract text from a cell:

- **TEXTBEFORE**:
Returns text that’s before delimiting characters
- **TEXTAFTER**:
Returns text that’s after delimiting characters
- **TEXTSPLIT**:
Splits text into rows or columns using delimiters

## 11 New Excel Functions for Dynamic Array Manipulation

Dynamic arrays have been the break trough of array formulas in Excel. Eleven new functions make working with dynamic arrays even more fun:

Functions to **combine arrays**:

- **VSTACK** - Stacks arrays vertically
- **HSTACK** - Stacks arrays horizontally

Functions to **shape arrays**:

- **WRAPROWS** - Wraps a row array into a 2D array
- **WRAPCOLS** - Wraps a column array into a 2D array
- **TOROW** - Returns an array as one row
- **TOCOL** - Returns an array as one column

Functions to **resize arrays**:

- **TAKE** - Returns rows or columns from an array start to end
- **DROP** - Drops rows or columns from an array start to end
- **CHOOSEROWS** - Returns the specified rows from an array
- **CHOOSECOLS** - Returns the specified columns from an array
- **EXPAND** - Expands an array to the specified dimensions

## Improvements in Excel for the Web

- **Conditional Formating Pane** - Microsoft enhanced the user experience for creating and managing conditional formatting rules in Excel for the Web. Now you can use a pane to inspect and manage the conditional formatting rules.
- **Function Library** - Microsoft added the function library to the formula menu. Now it is more consistent with the desktop experience. 
- **New filter menu** - The filter menu has been enhanced to make filtering data more convenient.
- **Insert slicer** - Now you can insert slicers for PivotTables and PivotCharts in Excel for the Web, too.
- **Insert online pictures** - With this feature, you can add images from Microsoft Stock images and from Bing search results to your worksheets.

## Improved Name Manager in Excel for Mac

The Name Manager in Excel for Mac was not on par with Excel for Windows. Not anymore. With this update you get all the capabilities you might have been missing.

## LAMBDA and LAMBDA helper functions are Generally Available for Production

In February 2022, Microsoft announced general availability for **LAMBDA** and the **LAMBDA helper functions**. With LAMBDA you can turn Excel formulas into custom functions. This revolutionizes how you can build formulas in Excel. Along with the GA Microsoft added an **Avanced Formula Environment**. This gives you a pane to edit more complicated Excel formulas in a proper editor. In addition, you can now use **function tool tips** and **auto-completion** with self-defined functions. In practice, your LAMBDA functions now look and feel like an native Excel function. Microsoft also increased the **recursion limit** by 16x. 

## Charting on the Web Feature Updates

Charting is a powerful tool in Excel to explore, analyze and present data. Charting in Excel for the Web was more like a viewer with only few editing capabilities. This has now changed. Microsoft has added a **Chart Format Pane** and **On-Chart Interactions** to Excel for the Web. You an also now **add and remove chart elements** and **create charts from non-adjacent cell ranges**.

## AutoComplete for Dropdown Lists in Excel for Windows

AutoComplete for dropdown lists matches the string you type in a dropdown list cell with words from items in the dropdown list. It then shows only the matching items. As you type more characters, the list gets smaller and smaller. It matches words anywhere in the list item string. 

This enhancement greatly speeds up data entry in fields with large lists. It also enables new use cases for this kind of data entry. 

At time of writing (April 2022) it is only available in the Beta Channel. As an upcoming enhancement before releasing for production, Microsoft plans to add excluding duplicates from the drop-down.

## Excel 4.0 (XLM) Macros are now Restricted by Default

You can now **enable or disable Excel 4.0 (XLM) macros in the Excel Trust Center** for enhanced security.
