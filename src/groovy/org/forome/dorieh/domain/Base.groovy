package org.forome.dorieh.domain

/**
 * Copyright (c) 2008 InterSystems, Corp.
 * Cambridge, Massachusetts, U.S.A.  All rights reserved.
 * Confidential, unpublished property of InterSystems.
 * <p>
 * @author <a href="mailto:mbouzin@intersystems.com">Michael A Bouzinier</a>
 * <p>
 * Date: 18/11/24
 * Time: 22:48
 *
 */
class Base
{
  protected Object currentContext = null

  protected static String addWithIndent(String body, int indent, String block)
  {
    String prefix = "  " * indent
    String text = prefix + block.replaceAll ("\n", "\n${prefix}")
    return body + text + "\n"
  }

  protected static String addText (String body, String key, String block, int indent)
  {
    if (block.contains ('\n')) {
      body = addWithIndent (body, indent, key + ": |")
      body = addWithIndent (body, indent + 1, block)
    } else {
      body = addElement (body, key, block, indent)
    }
    return body
  }

  protected static String addList (String body, String key, List<String> values, int indent)
  {
    body = addWithIndent (body, indent, key + ": ")
    for (String value: values) {
      body = addWithIndent (body, indent + 1, "- ${value}")
    }
    return body
  }

  protected static String addElement (String body, String key, String value, int indent)
  {
    if (value.contains ("\n"))
      return addText (body, key, value, indent)
    return addWithIndent (body, indent, key + ": " + value)
  }

  protected static void call (Closure closure, Object context)
  {
    closure.delegate = context
    closure.resolveStrategy = Closure.DELEGATE_FIRST
    closure.call()
  }


}
