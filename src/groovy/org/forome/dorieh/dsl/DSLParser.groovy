/*
 * Copyright (c) 2024. Harvard University
 *
 * Developed by Research Software Engineering,
 * Harvard University Research Computing and Data (RCD) Services.
 *
 * Author: Michael A Bouzinier
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

package org.forome.dorieh.dsl

import org.codehaus.groovy.control.CompilerConfiguration

class DSLParser {

  private static String preprocessDsl(dslScript) {
    def processedScript = new StringBuilder()
    dslScript.eachLine { line ->
      String prefix = indentation (line)
      if (line.trim().startsWith('-')) {
        def itemValue = line.trim().replaceFirst('-', '').trim()
        processedScript.append("${prefix}item ${itemValue}\n")
      } else {
        processedScript.append(line).append('\n')
      }
    }
    return processedScript.toString()
  }

  private static String indentation (String line) {
    def matcher = (line =~ /\S/)
    if (matcher) {
      return line.substring (0, matcher.start ())
    }
    return ""
  }


  static void parseGroovyScript(String filePath)
  {
    // Read the script content from a file
    File scriptFile = new File(filePath)

    if (!scriptFile.exists()) {
      throw new IllegalArgumentException("DSL Script file not found at specified path.")
    }

    String scriptContent = preprocessDsl (scriptFile.text)

    CompilerConfiguration config = new CompilerConfiguration()
    config.setScriptBaseClass(DSLScript.class.name)

    GroovyShell shell = new GroovyShell(new Binding(), config)

    Script parsedScript = shell.parse(scriptContent)
    parsedScript.run()
    DSLScript scriptInstance = (DSLScript) parsedScript
    Dataflow dslInstance = scriptInstance.dsl
    dslInstance.toYAML ()
  }
}

