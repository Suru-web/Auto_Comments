// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const axios = require('axios')

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "auto-comment-generator" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('auto-comment-generator.generate-comments', async () => {
		// The code you place here will be executed every time your command is executed

		const editor = vscode.window.activeTextEditor;
		let code = '';
		let language = '';

		if (editor) {
			code = editor.document.getText();
			language = editor.document.languageId; // 'python', 'cpp', 'java'
		} else {
			language = await vscode.window.showQuickPick(['python', 'cpp', 'java'], {
				placeHolder: 'Select the language for the code snippet'
			});

			code = await vscode.window.showInputBox({ prompt: 'Paste your code here' }) || '';
		}

		if (language == 'c') {
			language = 'cpp'
		}
		else if (language == 'c++') {
			language = 'cpp'
		}

		if (!code.trim()) {
			vscode.window.showErrorMessage("No code provided.");
			return;
		}
		const link = "http://127.0.0.1:5000/" + language
		console.log(link)
		const res = await axios.get(link, {
			params: { code }
		});
		const commentedCode = res.data.commented_code;

		const action = await vscode.window.showQuickPick(['Replace current file', 'Just preview'], {
			placeHolder: 'What would you like to do with the commented code?'
		});

		if (action === 'Replace current file' && editor) {
			editor.edit(editBuilder => {
				const fullRange = new vscode.Range(
					editor.document.positionAt(0),
					editor.document.positionAt(editor.document.getText().length)
				);
				editBuilder.replace(fullRange, commentedCode);
			});
		} else if (action === 'Just preview') {
			const doc = await vscode.workspace.openTextDocument({ content: commentedCode, language: 'python' });
			vscode.window.showTextDocument(doc);
		}
	});

	context.subscriptions.push(disposable);
}

exports.activate = activate;

// This method is called when your extension is deactivated
function deactivate() { }

module.exports = {
	activate,
	deactivate
}
